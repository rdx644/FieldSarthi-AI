"""User-approved public read-only judge role and explicit report allowlist."""

from alembic import op

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TABLE users DROP CONSTRAINT IF EXISTS users_check")
    op.execute("ALTER TABLE users DROP CONSTRAINT IF EXISTS users_role_check")
    op.execute(
        "ALTER TABLE users ADD CONSTRAINT users_role_check "
        "CHECK (role IN ('WORKER','SUPERVISOR','JUDGE'))"
    )
    op.execute(
        "ALTER TABLE work_orders ADD COLUMN IF NOT EXISTS "
        "judge_visible boolean NOT NULL DEFAULT false"
    )
    # User explicitly approved public transcript/audit publication in this session.
    # No future report is published automatically.
    op.execute("UPDATE work_orders SET judge_visible=true WHERE public_code='WO-AFF1E3EE3BD2'")


def downgrade() -> None:
    raise RuntimeError("Review database restoration before a destructive downgrade.")
