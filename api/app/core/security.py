from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from app.core.config import JWT_SECRET
from app.core.errors import AppError
from app.db.models import User
from app.db.session import get_db

password_hash = PasswordHash.recommended()
bearer = HTTPBearer(auto_error=False)


def token_for(user: User) -> str:
    return jwt.encode(
        {
            "sub": user.id,
            "exp": datetime.now(UTC) + timedelta(minutes=30),
            "iss": "fieldsaarthi",
            "aud": "fieldsaarthi-web",
        },
        JWT_SECRET,
        algorithm="HS256",
    )


def current_user(
    *,
    request: Request,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    try:
        if request.headers.get("Authorization") and not credentials:
            raise AppError(401, "UNAUTHENTICATED", "A valid bearer header is required.")
        token = (
            credentials.credentials if credentials else request.cookies.get("fieldsaarthi_session")
        )
        if not token:
            raise AppError(401, "UNAUTHENTICATED", "Please sign in to continue.")
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=["HS256"],
            issuer="fieldsaarthi",
            audience="fieldsaarthi-web",
            options={"require": ["exp", "sub", "iss", "aud"]},
        )
        user = db.get(User, payload["sub"])
        if not user or not user.is_active:
            raise AppError(401, "UNAUTHENTICATED", "Your session is no longer active.")
        return user
    except jwt.InvalidTokenError:
        raise AppError(401, "UNAUTHENTICATED", "Please sign in again.") from None


def worker(*, user: Annotated[User, Depends(current_user)]) -> User:
    if user.role != "WORKER":
        raise AppError(403, "FORBIDDEN", "This action is available to reporters.")
    return user


def supervisor(*, user: Annotated[User, Depends(current_user)]) -> User:
    if user.role != "SUPERVISOR":
        raise AppError(403, "FORBIDDEN", "Supervisor access is required.")
    return user
