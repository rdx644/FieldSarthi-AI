# Operations

## Public judge access and rollback

`PUBLIC_JUDGE_DEMO_ENABLED=true` enables the user-approved read-only judge session.
The flag is off in the local example and on in the submission Blueprint. The user
approved publishing WO-AFF1E3EE3BD2; other reports default to private. This flag is
owned by the participants and should be reviewed at the end of the challenge demo.
Set it to false to deny both new and existing judge sessions. No team password is
published; judges cannot mutate reports or call billable speech endpoints.

Before rolling back to code older than migration 0004, first disable the flag and
deactivate JUDGE users in the database with the authorized operator connection:

```sql
UPDATE users SET is_active=false WHERE role='JUDGE';
```

Verify existing judge cookies receive 401, then deploy the compatible earlier
image. **Do not roll back first:** old queue authorization does not recognize
JUDGE and could give an active judge session broader visibility. Preserve the
additive source/publication columns and immutable migrations; do not downgrade or
delete orders. Re-enable the account only after the current authorization code is
restored and its tests pass. Also verify private MANUAL_TEXT orders are not
mislabelled by an older UI; prefer fixing forward for source-display problems.

## Stage diagnostics

The operator questions are: did decoding fail, did Gnani fail or become slow, and
did extraction finish? Correlated `stage_completed` JSON events answer these for
`audio_normalize`, `provider_stt`, `extraction`, and `provider_tts`. Events contain
elapsed time, safe error code and actual returned STT request/model metadata;
never request bodies, passwords, raw audio or transcripts. Readiness also checks
that the database migration heads match this build, and never calls Gnani.
The explicit MANUAL_TEXT accessibility route requires human confirmation and
never invents a provider result.

## Existing Windows local instance
The private isolated PostgreSQL 18 cluster is `private/postgres-data`, bound to 127.0.0.1:55432. Never use another project's database.
```powershell
& 'C:\Program Files\PostgreSQL\18\bin\pg_ctl.exe' -D C:\Users\putit\fieldsaarthi-ai\private\postgres-data status
# Only if stopped:
& 'C:\Program Files\PostgreSQL\18\bin\pg_ctl.exe' -D C:\Users\putit\fieldsaarthi-ai\private\postgres-data -l C:\Users\putit\fieldsaarthi-ai\private\postgres.log -o '-p 55432 -h 127.0.0.1' -w start
```
Build web, sync api, migrate and seed as README describes. Read `private/demo-accounts.json` locally for passwords; never screen-share it. Existing seeds leave passwords unchanged. A fresh production database requires the three private demo password variables. Keep JWT/Gnani/database secrets in the host secret manager.

Liveness `/health/live`; readiness `/health/ready` checks a migrated reachable DB, never spends Gnani credits. JSON app logs contain generated request IDs, methods, statuses and timings, never bodies. Correlate user-visible error request IDs with logs. API errors are typed; raw provider payloads do not reach users. 401: sign in again; 403: role/CSRF; 409: refresh version/review conflict; 422: correct fields/audio; 429: budget/login throttle; 503: provider unavailable. No manual fake transcript fallback.

## Backup and rollback
`uv run python -m scripts.backup_drill` makes a private pg_dump and restores it to a **new scratch database**, comparing row counts. It never drops or overwrites the source. `docs/evidence/backup-restore.json` records the executed drill. Scratch database and dump are retained privately. On another platform set PG_BIN or provide pg_dump/pg_restore on PATH. Treat dumps as sensitive; they contain user hashes and transcripts.

Rollback application code to the prior verified commit/image with a compatible schema. Migrations are additive; destructive downgrades deliberately refuse. For database recovery, restore a reviewed backup into a new instance and verify counts/invariants before switching the secret connection URL. Do not delete production rows to reset a demo.

## Limits and privacy
Single worker/replica, 20 sign-in attempts per IP/15 minutes, 24 provider calls per user/hour and 80 per process/hour. In-memory counters reset on restart and are not an account-wide credit guarantee; monitor the actual Gnani console. Clips target 25 seconds, provider maximum 30; local upload cap 10 MiB. Temporary decoded audio is removed in finally blocks. Existing consented test clips in private/ are operator test assets, not app storage; remove after the evidence/submission review unless continued retention is consented.

Render free services can sleep/cold-start and their files are ephemeral; DB storage is separate. Free PostgreSQL expires after 30 days. The prepared plan is for a submission demo, not a production availability or backup SLA.
