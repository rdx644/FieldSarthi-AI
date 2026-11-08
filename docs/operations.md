# Operations
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
