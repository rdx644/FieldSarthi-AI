# ADR-010: Durable admission of speech operations

Status: Implemented and verified locally on 2026-11-14; production rollout held.
Trace: IMP-05; FR-03/06/09/23; NFR-01/04/05/09/10/13.

## Decision

An additive `0005` migration creates `provider_admissions`, containing only a UUID,
actor foreign key, operation (`STT` or `TTS`) and database UTC admission time.
There are no transcripts, audio, keys, response bodies or monetary estimates.
Indexes cover time and actor/time; the migration revokes table access from PUBLIC.
The existing database owner remains privileged; no public ledger endpoint exists.

After authorization and the operator pause check, a short independent transaction
checks the actor is active and has a worker/supervisor role, takes the fixed global
PostgreSQL advisory transaction lock `6114542871`, reads database time, and counts
the rolling preceding hour. At most 24 operations per actor and 80 globally are
admitted across STT and TTS. It commits the reservation before any network wait.
Database or commit failure returns a sanitized `503 PROVIDER_BUDGET`; quota denial
returns `429 PROVIDER_BUDGET`. There is no process-memory fallback. A reservation
is retained if processing subsequently fails, so errors cannot reclaim quota.

Both async routes offload synchronous reservation work to Starlette's worker pool.
Lock waiting is bounded to three seconds and each SQL statement to five seconds.
The lock is released before the provider semaphore/network wait. Existing bounded
audio decoding happens before STT reservation, so invalid clips do not consume it.
An early flag-only pause check precedes audio reading/normalization; it closes the
upload on denial, and reservation checks the pause flag again. A paused corrupt
clip returns `GNANI_REQUESTS_PAUSED` without decoder, ledger or provider work.
No reservation is made for manual intake, read-only operations or judge requests.

An operator can invoke `cleanup_provider_admissions()` through an authorized local
maintenance context. Each invocation removes at most 500 rows older than seven
days and preserves recent quota history. Cleanup is never run on request traffic.

These are operation admissions, not exact upstream attempt counts or credit caps.
The current STT adapter defaults to one retry (up to two upstream requests per
admitted operation), and allows explicitly constructed clients with two retries
(up to three). The TTS adapter makes one upstream request. No retry policy changed.
`GNANI_REQUESTS_ENABLED=false` remains independent of database availability.
One application worker/replica and the existing provider semaphore remain required;
durable quotas alone do not authorize horizontal scaling.

## Local verification

`tests/integration/test_provider_admission.py` verifies real PostgreSQL concurrent
actor/global admission, both operation types, a separate Python process observing
already-exhausted quota, expiry, bounded cleanup, inactive/judge denial, failed
commit rollback, database outage without provider calls or saved-order changes,
and preservation of order detail/audit/provenance on a simulated 0004 upgrade.
Existing pause, release-guard and legacy upgrade regressions pass. All provider
behavior in these tests is explicitly stubbed; zero paid requests were made.

## Rollout and rollback constraint

The new table is additive, and existing domain queries remain compatible. However,
the prior application requires database migration head exactly `0004`; it reports
not-ready against a `0005` database. The candidate derives the new exact head from
Alembic and reports ready at `0005`. The test reproduces the old exact-head check;
it is not a hosted rollback rehearsal or a previous-image deployment.

There is a second startup constraint: the inspected previous startup entrypoint
runs `alembic upgrade head` before serving. Its older migration tree does not
contain revision `0005`, so it cannot resolve a database already stamped `0005`.
This is reasoning from the inspected startup code and migration graph, not an
executed previous-image boot test. A rollback compatibility release must handle
both startup migration resolution and readiness before the schema is advanced.

**Production deployment is blocked** until a staged compatibility release is
reviewed and verified against the exact previous application image, with a private
backup and explicit deployment approval. Do not bypass readiness or mark all future
migration heads compatible. Never delete the ledger or down-migrate a live database
to make rollback appear successful. No production migration, deploy, account
rotation, access-policy change, fresh recording or paid speech evaluation was done.

Public synthetic logins remain intentionally shared under existing authorization.
The login throttle remains process-local. A separate scoped fix holds a mutex only
around its existing prune/check/append sequence; the existing 20 attempts per
address per 15 minutes and 10,000-address bound are unchanged. It releases the
mutex before database queries or password hashing. A deliberately interleaved
two-thread regression reproduced 21 admitted attempts from a starting count of
19 before the fix; the mutex admits one and rejects the other. Additional tests
cover 40 concurrent attempts, map capacity and expiry. The ledger does not cover
login attempts, and no proxy or forwarded-header trust settings changed.

The existing `api/scripts/start.py` uses Uvicorn `--proxy-headers` together with
`--forwarded-allow-ips '*'`. Consequently `request.client.host`, which keys login
throttling, relies on forwarded headers and the deployment assumption that ingress
passes exclusively through a trusted proxy which replaces/sanitizes them. The
application itself does not validate that boundary. Direct access or unsanitized
forwarded headers could undermine address-based throttling. This change preserves
the current deployment policy; verifying Render ingress behavior or narrowing
trusted proxy peers is a separate operator-reviewed change, not established by
these local limiter tests.


## November 15 exact previous-source verification

The [fresh compatibility check](../evidence/improvement-rollback-compatibility.json)
executed the API source from actual deployed commit `85e1a5e` against only
`fieldsaarthi_test` at `0005`. Its startup `alembic upgrade head` failed to resolve
`0005` and its real `/health/ready` returned 503. No domain writes or provider calls
were made. This confirms the previously reasoned blocker; it is not a built-image
or hosted rollback rehearsal. A staged compatible rollback image, exact CI,
approved backup and deployment remain mandatory before any production migration.


## Compatibility blocker resolved locally

The [finalisation design](../release-finalisation.md) and
[real two-image rehearsal](../evidence/improvement-container-release.json) now
provide a separate paused previous-app build that starts at exactly 0004 or 0005
without migrating, plus a strict 0005 candidate. Stage -> activate -> rollback ->
restore passed with seven domain tables and two admission rows unchanged. The
original unmodified 85e1a5e image remains incompatible; use the newly prepared,
reviewed rollback artifact. Production backup/approval and exact source CI remain
required before deployment. Earlier reasoned and failed-source checks above are
historical and are not altered.
