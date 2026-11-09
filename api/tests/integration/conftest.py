import pytest
from alembic.config import Config
from sqlalchemy import text

from alembic import command
from app.db.session import SessionLocal, engine
from app.seed import seed


@pytest.fixture(scope="session", autouse=True)
def migrated_database():
    assert engine.url.database == "fieldsaarthi_test", "Never reset a non-test database"
    command.upgrade(Config("alembic.ini"), "head")


@pytest.fixture
def accounts(migrated_database):
    from app.core.limits import provider_budget
    from app.routers.auth import attempts

    attempts.clear()
    provider_budget.entries.clear()
    assert engine.url.database == "fieldsaarthi_test"
    with engine.begin() as connection:
        connection.execute(text("DROP SCHEMA public CASCADE"))
        connection.execute(text("CREATE SCHEMA public"))
    command.upgrade(Config("alembic.ini"), "head")
    with SessionLocal() as db:
        return seed(db)
