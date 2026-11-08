from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL, pool_pre_ping=True, hide_parameters=True)
SessionLocal = sessionmaker(engine, expire_on_commit=False)


def get_db() -> Generator[Session]:
    with SessionLocal() as session:
        yield session
