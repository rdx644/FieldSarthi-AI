Current hosted completion - 2026-11-15: **migration, rollback and restoration
verified on Render**, application `241a063`. All 14 saved report details, audit
histories and original provider facts match the private pre-deploy baseline.
The sole approved judge report remains OPEN/version 1 with its original transcript,
provider provenance and one audit event. Hosted queue summaries reconcile with
saved data; six actual Chrome judge views pass accessibility/layout/keyboard
checks. No new Gnani calls or report mutations were made.

The participant confirmed a current restore-ready backup, then the service passed
compatibility stage at 0004 -> candidate at 0005 -> compatibility rollback at 0005
-> candidate restoration at 0005. Live speech was subsequently restored following
the participant's explicit current-balance confirmation. Automatic deployment
remains off. Direct SQL/SSH was unavailable; schema proof uses the exact deployed
source's database-backed readiness checks. Backup retention and the December 9
free-database expiry remain participant-owned. Independent audio evaluation is
still explicitly deferred; no 95/100 result is claimed.

See [current hosted evidence](evidence/improvement-hosted-release.json). Earlier checkpoints below retain their
historical scope and are superseded where they describe deployment/backup gates.

Latest ownership update: production backup is handled by the participant and
completion is not yet confirmed. The agent completes automatic source publication,
protected merge, CI and local/main synchronization. Engineering and image rollback
are verified; live migration waits for backup confirmation. See
[current status](release-finalisation.md). Earlier checkpoint statements below retain their scope.

Latest finalisation: **307 backend tests and actual container compatibility,
rollback and restoration pass locally**; independent evaluation is explicitly
participant-deferred. The prepared compatibility build resolves the earlier local
blocker. Both source CI runs pass; approved production backup/deployment remains pending.
See [current finalisation](release-finalisation.md). Earlier checkpoint statements below retain their
historical scope.

# Operations

## Public judge access and rollback

`PUBLIC_JUDGE_DEMO_ENABLED=true` enables the user-approved read-only judge session.
The flag is off in the local example and on in the submission Blueprint. The user
approved publishing WO-AFF1E3EE3BD2; other reports default to private. This flag is
owned by the participants and should be reviewed at the end of the challenge demo.
Set it to false to deny both new and existing judge sessions. Judge entry needs
no password; judges cannot mutate reports or call billable speech endpoints. The
three shared synthetic team logins are intentionally public in README under the
participant's existing policy; provider, database, JWT and hosting secrets remain
private. Activity through those team accounts is shared demo data.

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
Single worker/replica, 20 sign-in attempts per IP/15 minutes. The local IMP-05 candidate uses durable 24-per-actor/80-global hourly STT/TTS operation admissions; the prior deployed limiter resets on restart. Login throttling remains process-local, with its thread race fixed in the candidate. Admission counts are not an account-wide credit guarantee; monitor the actual Gnani console. Clips target 25 seconds, provider maximum 30; local upload cap 10 MiB. Temporary decoded audio is removed in finally blocks. Existing consented test clips in private/ are operator test assets, not app storage; remove after the evidence/submission review unless continued retention is consented.

Render free services can sleep/cold-start and their files are ephemeral; DB storage is separate. Free PostgreSQL expires after 30 days. The prepared plan is for a submission demo, not a production availability or backup SLA.

## Temporary demo credit control ? NFR-13

`GNANI_REQUESTS_ENABLED=false` pauses both STT and TTS before any provider call, returning `503 GNANI_REQUESTS_PAUSED`. Existing reports, manual text reporting, confirmation and supervisor actions remain available. The TTS capability also becomes false. Unset defaults to true for compatibility; an explicit value other than true pauses calls. An environment change on Render needs a deploy before the running process sees it. Check readiness afterwards; no paid smoke is needed to verify the flag.

Before opening the demo, check the actual remaining balance in https://app.gnani.ai/voice/usage and record the value and UTC/IST timestamp privately. Recheck after a demo session and before re-enabling a paused service. Pause when balance is exhausted, uncertain or below the operator's chosen reserve. A 402 provider response remains a failed request, never success. This app does not invent a price per request, account balance or undocumented balance API.

The local candidate's shared 24-per-actor/80-global rolling-hour admission ledger covers both STT and TTS and survives restarts. Failed processing retains reservations. Default STT retries permit up to two upstream attempts per operation (explicitly constructed adapters can allow three); TTS makes one. Other uses of the key are outside this ledger. The prior deployed RAM limiter resets on restart. These are operation controls, not money. Optional operator maintenance `app.services.provider_admission.cleanup_provider_admissions()` deletes at most 500 entries older than seven days per invocation; it is not called on request traffic. Follow [ADR-010](adrs/ADR-010-durable-provider-admission.md) and the [deployment compatibility gate](deployment.md#november-14-candidate-gate) before any migration. Balance checks, chosen reserve, backup retention and current expiry remain operator-owned; no paid upgrade was performed.

## Executed compatible rollback

The [operational release drill](evidence/demo-operational-release.json) deployed verified application `85e1a5e20c1f623c0ce664493c8f002e7d5cff10`, rolled back via Render to the prior judge-safe `6f702c2` artifact, and restored the new artifact. All 12 existing report-detail hashes, including raw/provider/corrected facts and audit events, matched at every phase. The approved public report stayed OPEN/version 1 and was the only judge-visible report. No schema downgrade, report mutation or Gnani request was used. This validates these compatible revisions only; retain the pre-0004 judge-safety precautions above.

## November 15 read-only status

The operator API confirms the original application is still live and the free database expires on 2026-12-09T12:16:30.004422Z; both health endpoints returned 200. The only approved judge sample remains OPEN/version 1 with unchanged original transcript hash. These checks spent no speech credits and made no domain writes. Candidate release, backup/restore, direct schema verification and real credit observation remain gated; see [the current handoff](improvement-handoff.md).
