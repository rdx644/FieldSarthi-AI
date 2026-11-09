"""Add explicit manual accessibility provenance without relabeling voice reports."""

from alembic import op

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 0001 historically creates current ORM metadata on fresh installations.
    op.execute(
        "ALTER TABLE report_intakes ADD COLUMN IF NOT EXISTS source_type "
        "varchar(20) NOT NULL DEFAULT 'GNANI_STT'"
    )
    op.execute(
        "ALTER TABLE report_intakes ADD CONSTRAINT intake_source_type "
        "CHECK (source_type IN ('GNANI_STT','MANUAL_TEXT'))"
    )
    op.execute(
        "ALTER TABLE report_intakes ADD CONSTRAINT manual_has_no_speech_provenance "
        "CHECK (source_type <> 'MANUAL_TEXT' OR (provider_model IS NULL AND "
        "provider_request_id IS NULL AND audio_duration_seconds IS NULL "
        "AND stt_latency_ms IS NULL))"
    )
    op.execute("""CREATE OR REPLACE FUNCTION protect_transcript()
    RETURNS trigger LANGUAGE plpgsql AS $$
    BEGIN
      IF NEW.source_type IS DISTINCT FROM OLD.source_type OR
        (OLD.raw_transcript IS NOT NULL AND
          (NEW.raw_transcript IS DISTINCT FROM OLD.raw_transcript OR
           NEW.provider_model IS DISTINCT FROM OLD.provider_model OR
           NEW.provider_request_id IS DISTINCT FROM OLD.provider_request_id OR
           NEW.language_code IS DISTINCT FROM OLD.language_code OR
           NEW.audio_duration_seconds IS DISTINCT FROM OLD.audio_duration_seconds OR
           NEW.stt_latency_ms IS DISTINCT FROM OLD.stt_latency_ms OR
           NEW.extraction::jsonb IS DISTINCT FROM OLD.extraction::jsonb)) THEN
        RAISE EXCEPTION 'provider provenance is immutable';
      END IF;
      RETURN NEW;
    END; $$""")


def downgrade() -> None:
    raise RuntimeError("Review database restoration before a destructive downgrade.")
