"""WBS-02 initial schema and database-enforced provenance/audit protection."""

from alembic import op
from app.db.models import Base

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    Base.metadata.create_all(bind=op.get_bind())
    op.execute("""CREATE FUNCTION protect_audit() RETURNS trigger LANGUAGE plpgsql AS $$
    BEGIN RAISE EXCEPTION 'audit events are immutable'; END; $$""")
    op.execute("""CREATE TRIGGER immutable_audit BEFORE UPDATE OR DELETE ON audit_events
                   FOR EACH ROW EXECUTE FUNCTION protect_audit()""")
    op.execute("""CREATE FUNCTION protect_transcript() RETURNS trigger LANGUAGE plpgsql AS $$
    BEGIN
      IF OLD.raw_transcript IS NOT NULL AND
        (NEW.raw_transcript IS DISTINCT FROM OLD.raw_transcript OR
         NEW.provider_model IS DISTINCT FROM OLD.provider_model OR
         NEW.provider_request_id IS DISTINCT FROM OLD.provider_request_id) THEN
        RAISE EXCEPTION 'provider provenance is immutable';
      END IF;
      RETURN NEW;
    END; $$""")
    op.execute("""CREATE TRIGGER immutable_provenance BEFORE UPDATE ON report_intakes
                   FOR EACH ROW EXECUTE FUNCTION protect_transcript()""")


def downgrade() -> None:
    raise RuntimeError("Destructive downgrade blocked. Restore a reviewed backup instead.")
