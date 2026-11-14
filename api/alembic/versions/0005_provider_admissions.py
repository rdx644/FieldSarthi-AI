"""IMP-05 additive operation ledger; no domain rows or provenance are rewritten."""

from alembic import op

revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 0001 uses current Base metadata for a fresh database; existing 0004 databases
    # need the same additive table. Re-running the migration is safe in either case.
    op.execute("""CREATE TABLE IF NOT EXISTS provider_admissions (
        id varchar(36) PRIMARY KEY,
        actor_id varchar(36) NOT NULL REFERENCES users(id),
        operation varchar(3) NOT NULL CHECK (operation IN ('STT', 'TTS')),
        admitted_at timestamptz NOT NULL DEFAULT clock_timestamp()
    )""")
    op.execute("""CREATE INDEX IF NOT EXISTS ix_provider_admissions_admitted_at
                  ON provider_admissions (admitted_at)""")
    op.execute("""CREATE INDEX IF NOT EXISTS ix_provider_admissions_actor_time
                  ON provider_admissions (actor_id, admitted_at)""")
    op.execute("REVOKE ALL ON TABLE provider_admissions FROM PUBLIC")


def downgrade() -> None:
    raise RuntimeError(
        "Preserve admission history; use a reviewed compatible application rollback."
    )
