"""Protect maintenance operations as well as row updates."""

from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""CREATE TRIGGER immutable_audit_truncate BEFORE TRUNCATE ON audit_events
                   FOR EACH STATEMENT EXECUTE FUNCTION protect_audit()""")
    op.execute("""CREATE FUNCTION protect_intake_delete() RETURNS trigger LANGUAGE plpgsql AS $$
    BEGIN
      IF TG_OP = 'TRUNCATE' THEN
        RAISE EXCEPTION 'provider provenance is immutable';
      END IF;
      IF OLD.raw_transcript IS NOT NULL THEN
        RAISE EXCEPTION 'provider provenance is immutable';
      END IF;
      RETURN OLD;
    END; $$""")
    op.execute("""CREATE TRIGGER immutable_intake_delete BEFORE DELETE ON report_intakes
                   FOR EACH ROW EXECUTE FUNCTION protect_intake_delete()""")
    op.execute("""CREATE TRIGGER immutable_intake_truncate BEFORE TRUNCATE ON report_intakes
                   FOR EACH STATEMENT EXECUTE FUNCTION protect_intake_delete()""")


def downgrade() -> None:
    raise RuntimeError("Review database restoration before a destructive downgrade.")
