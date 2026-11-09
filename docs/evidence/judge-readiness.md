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

Verified locally: **159 backend tests**, strict mypy, Ruff lint/format, TypeScript/Vite
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

CI now scans all reachable commit history and the index for forbidden private/raw
media paths and known credential signatures, including merge-resolution paths.
This bounded scanner supplements review; it does not claim universal secret detection.
CI also runs the complete non-billable fixture-provider browser workflow and saves
its evidence as an artifact. Current remote CI/deployment outcomes will be recorded
after they execute; the previous hosted evidence remains historical proof.

NFR-01 automated test: ten consecutive complete API workflows using test-only
speech results, genuine decoding/PostgreSQL writes, explicit review/confirmation,
idempotent replay, supervisor assignment/priority/start/resolution and durable
read-back. This verifies application reliability under controlled inputs; it is
not an upstream availability, ASR accuracy or fresh human recording claim.

The user explicitly approved public read-only publication of WO-AFF1E3EE3BD2 and
authorized bounded paid evaluation/verification requests. Team passwords stay
private. New reports do not become public automatically.

Still participant-owned: the 15 authentic recordings and reviewed ground truth,
individual eligibility/contributions, final 2–3 minute video/public post, release
review and the user-reserved final form. The runner and guide are ready; no audio
score is claimed until actual recordings have been evaluated. Managed backup and
30-day database limitations remain explicit; no paid hosting upgrade is assumed.
