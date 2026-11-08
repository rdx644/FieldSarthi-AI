import threading
import time
from collections import defaultdict, deque
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request, Response
from pwdlib.exceptions import UnknownHashError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import APP_ENV
from app.core.errors import AppError
from app.core.security import current_user, password_hash, supervisor, token_for
from app.db.models import Asset, Location, User
from app.db.session import get_db
from app.schemas.commands import Login

router = APIRouter(prefix="/api/v1")
attempts: dict[str, deque[float]] = defaultdict(deque)
dummy_hash = password_hash.hash("not-a-valid-demo-password")
hash_slots = threading.BoundedSemaphore(2)


def user_json(user: User) -> dict[str, Any]:
    return {
        "id": user.id,
        "display_name": user.display_name,
        "email": user.email,
        "role": user.role,
    }


@router.post("/auth/login")
def login(
    *, body: Login, request: Request, response: Response, db: Annotated[Session, Depends(get_db)]
) -> dict[str, Any]:
    address = request.client.host if request.client else "unknown"
    now = time.monotonic()
    for key in list(attempts):
        while attempts[key] and attempts[key][0] < now - 900:
            attempts[key].popleft()
        if not attempts[key]:
            del attempts[key]
    if len(attempts) >= 10000 and address not in attempts:
        raise AppError(429, "RATE_LIMITED", "Please try again later.")
    if len(attempts[address]) >= 20:
        raise AppError(429, "RATE_LIMITED", "Too many sign-in attempts. Try again in 15 minutes.")
    attempts[address].append(now)
    user = db.scalar(select(User).where(User.email == body.email.lower()))
    if not hash_slots.acquire(timeout=1):
        raise AppError(429, "SIGN_IN_BUSY", "Sign-in is busy. Please try again.")
    try:
        try:
            valid = password_hash.verify(body.password, user.password_hash if user else dummy_hash)
        except UnknownHashError:
            valid = False
    finally:
        hash_slots.release()
    if not valid or not user or not user.is_active:
        raise AppError(401, "INVALID_CREDENTIALS", "The email or password is incorrect.")
    token = token_for(user)
    response.set_cookie(
        "fieldsaarthi_session",
        token,
        max_age=1800,
        httponly=True,
        secure=APP_ENV == "production",
        samesite="strict",
        path="/",
    )
    return {"access_token": token, "token_type": "bearer", "user": user_json(user)}


@router.post("/auth/logout")
def logout(response: Response) -> dict[str, bool]:
    response.delete_cookie("fieldsaarthi_session", path="/")
    return {"ok": True}


@router.get("/me")
def me(*, user: Annotated[User, Depends(current_user)]) -> dict[str, Any]:
    return user_json(user)


@router.get("/auth/session")
def session_status(
    request: Request, response: Response, db: Annotated[Session, Depends(get_db)]
) -> dict[str, Any]:
    if not request.cookies.get("fieldsaarthi_session"):
        return {"user": None}
    try:
        user = current_user(request=request, credentials=None, db=db)
        return {"user": user_json(user)}
    except AppError:
        response.delete_cookie("fieldsaarthi_session", path="/")
        return {"user": None}


@router.get("/locations")
def locations(
    *, user: Annotated[User, Depends(current_user)], db: Annotated[Session, Depends(get_db)]
) -> list[dict[str, Any]]:
    return [
        {"id": x.id, "code": x.code, "name": x.name}
        for x in db.scalars(select(Location).where(Location.is_active).order_by(Location.code))
    ]


@router.get("/assets")
def assets(
    *,
    location_id: str | None = None,
    user: Annotated[User, Depends(current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> list[dict[str, Any]]:
    query = select(Asset).where(Asset.is_active)
    if location_id:
        query = query.where(Asset.location_id == location_id)
    return [
        {"id": x.id, "asset_code": x.asset_code, "name": x.name, "location_id": x.location_id}
        for x in db.scalars(query.order_by(Asset.asset_code))
    ]


@router.get("/users")
def users(
    *, user: Annotated[User, Depends(supervisor)], db: Annotated[Session, Depends(get_db)]
) -> list[dict[str, Any]]:
    return [
        user_json(x) for x in db.scalars(select(User).where(User.is_active, User.role == "WORKER"))
    ]
