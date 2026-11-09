# Judge readiness completion evidence

Baseline: e8d6f97, 2026-11-09. The four supplied branches are already ancestors of
main: docs/human-microphone-proof, docs/render-hosted-proof,
chore/roadmap-audit-render, feature/complete-fieldsaarthi. No history rewrite or
duplicate branch merge is needed. New work proceeds through a protected PR.

The original roadmap/audit remain unchanged historical baselines. This completion
record supersedes their implementation/test-gap observations where evidence below
exists; it does not turn participant tasks into passed gates.

Implemented: exact source spans/parser version and conservative ambiguity handling;
MANUAL_TEXT source with no false Gnani metadata and immutable provenance; typed
OpenAPI response contracts; actionable STT errors; explicit Gnani/retention disclosure;
priority/location/assignee filters; cancellation reason/audit; stage telemetry;
exact migration-head readiness; user-approved read-only public judge role and report
allowlist, with immediate flag-based session revocation.

Verified locally: **190 backend tests**, strict mypy, Ruff lint/format, TypeScript/Vite
build and frontend lint/Prettier. Backend/frontend dependency audits report no known
vulnerabilities. The retained six-view accessibility check passes. The new
[full browser regression](browser-regression/results.json) passes ten axe/layout
checks at 320/768/1024/1440 widths with no JS errors, testing permission-denied
guidance, manual source labelling, malicious transcript escaping, explicit
confirmation, replay, supervisor resolution/refresh and public judge viewing.
Its speech result is explicitly a test-only fixture; live provider calls: zero.

A fresh local pg_dump → new scratch database restore has matching seven-table
counts; [result](backup-restore.json). The judge allowlist mutation experiment
removed its access check, observed the focused test fail, restored exact source
bytes, and reran the focused tests successfully (2 passed). Independent review
also found and closed existing-session revocation, stale detail-page state,
cached-response recovery, safety-score and historical-path scanning defects.

PR review additionally reproduced and fixed the legacy `users_check` migration
constraint and missing duplicate hints for typed reports. The actual hosted
snapshot was privately exported with explicit user approval, restored locally and
upgraded from 0002 to 0004; judge seeding succeeds, only the approved report is
published, and its OPEN/version-1 state and original transcript hash remain intact.
See [hosted snapshot restore](hosted/release-backup-restore.json) and
[actual snapshot upgrade](hosted/snapshot-upgrade.json). The production database
was not migrated by this drill; its original IP allowlist was restored.

CI now scans all reachable commit history and the index for forbidden private/raw
media paths and known credential signatures, including merge-resolution paths.
This bounded scanner supplements review; it does not claim universal secret detection.
CI also runs the complete non-billable fixture-provider browser workflow and saves
its evidence as an artifact. Protected PR #8 merged at application commit
`6f702c26f5d0ebca99cc71ba870bb7031fdd4dcd`; its
[exact main CI passed](https://github.com/rdx644/FieldSarthi-AI/actions/runs/42682797881).
That application commit is live in deployment `dep-dbp1rkek1f9s73aqchvg`, Blueprint
GNANI in_sync. [Hosted authorization/health checks](hosted/judge-release-verification.json)
and [deployed browser checks](hosted/judge-browser-verification.json) pass. The public
judge button requires no password and exposes only the explicitly approved report.

[Ten consecutive genuine hosted workflows](hosted/reliability.json) passed with ten
actual Prisma requests, confirmation, replay, assignment/start/resolution and durable
read-back. One consenting clip was repeated: this verifies workflow reliability,
not distinct-clip ASR accuracy. [One genuine Timbre request](hosted/judge-release-tts.json)
returned valid WAV without changing the saved order/audit. A
[controlled restart](hosted/judge-release-restart.json) retained all ten workflow IDs,
states, versions, provider metadata and audit counts. The approved OPEN report also
retained its original transcript hash. Health and restart checks spent no credits.
The earlier hosted artifacts remain clearly labelled historical proof.

NFR-01 automated test: ten consecutive complete API workflows using test-only
speech results, genuine decoding/PostgreSQL writes, explicit review/confirmation,
idempotent replay, supervisor assignment/priority/start/resolution and durable
read-back. This verifies application reliability under controlled inputs; it is
not an upstream availability, ASR accuracy or fresh human recording claim.

The user explicitly approved public read-only publication of WO-AFF1E3EE3BD2 and
authorized bounded paid evaluation/verification requests. Team passwords stay
private. New reports do not become public automatically.

The participant recorded all 15 distinct clips through the local microphone
wizard and confirmed them ready. The genuine Prisma v2.5 development evaluation
scored **12/15 complete cases**, with all six required safety cases blocked.
Cases 04/10 use participant-approved English equivalents; actual coverage is
Hindi/English/Hinglish and Tamil remains unverified. Three ASR failures still
require human correction. Two initial transport failures were preserved and
recovered; cached successes were never resent for reassurance. Initial rules-v3
9/15 results are preserved beside the final rules-v4 result. These rules were
refined using the same development corpus: no held-out/WER/CER claim.
See [final metrics/confusion tables](audio-evaluation.json) and [initial result](audio-evaluation-rules-v3.json).

The final roadmap recheck independently covered 24 sections, 94 numbered headings
and 64 WBS tasks. It additionally closed hazard cue warnings, deferred/duplicate/
stale-stop microphone lifecycle races, selected-language disclosure, direct SQL
FK/check failures, SQL-injection negatives, provider-error scoring and stale CI
artifact risks. Original roadmap/submission materials remain excluded from Git;
reference copies are retained only under ignored private/reference.

Still participant-owned: individual eligibility/contributions, final 2–3 minute
video/public post, release review and the user-reserved final form. Managed backup
and 30-day database limitations remain explicit; no paid hosting upgrade is assumed.
