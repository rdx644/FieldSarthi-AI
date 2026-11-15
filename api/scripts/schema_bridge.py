"""Read-only startup gate for the temporary previous-application rollback build."""

from sqlalchemy import text

from app.db.session import engine

ALLOWED_HEADS = ({"0004"}, {"0005"})


def validate_bridge_schema() -> None:
    with engine.connect() as connection:
        connection.execute(text("SET TRANSACTION READ ONLY"))
        connection.execute(text("SET LOCAL statement_timeout = '5s'"))
        versions = set(connection.scalars(text("SELECT version_num FROM alembic_version")))
    if versions not in ALLOWED_HEADS:
        raise RuntimeError("The compatibility build requires exactly schema 0004 or 0005.")


if __name__ == "__main__":
    try:
        validate_bridge_schema()
    except Exception:
        raise SystemExit(
            "Compatibility schema check failed; no migration or seed was run."
        ) from None
