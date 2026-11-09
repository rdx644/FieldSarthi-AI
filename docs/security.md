# Security and privacy boundaries - development candidate

Scope: React/FastAPI development candidate at `8146882`, including genuine Prisma/Timbre adapters, PostgreSQL and Render configuration. This supersedes the initial WBS-01-only description. It is not a penetration-test or privacy-compliance certification.

Assets are provider credentials/credits, sessions/password hashes, synthetic reports, consenting audio and truthful provenance. Untrusted inputs cross browser -> API, media -> FFmpeg, provider -> strict response parser, and command -> database boundaries. The backend and PostgreSQL own persisted facts.

- Gnani credentials remain server-side. Fixed HTTPS endpoints, no redirects, bounded responses/time/retries and typed errors prevent raw provider-payload disclosure. No production fixture adapter exists.
- Argon2 passwords; short-lived signed JWT; HTTP-only SameSite=strict cookies, Secure in production; Origin plus X-Requested-With on cookie mutations. Every protected request verifies the current active DB identity/role. Malformed bearer auth cannot fall back to cookies.
- Worker ownership covers intake/order reads/writes, queue, duplicate hints and TTS. Supervisor mutations require the verified role. ORM binding and Pydantic commands constrain input.
- React renders text without unsafe HTML. CSP, frame denial, no-sniff, no-store API responses and microphone permission policy are applied.
- The request cap precedes multipart parsing. Media signatures and actual decoded sample count replace trust in names/MIME/duration. FFmpeg uses a fixed executable, argument array, restricted protocols, deadline, output-duration bound, two slots and temporary-directory cleanup.
- Advisory/intake/order locks, unique intake and idempotency constraints protect atomic order/audit writes. Audit/original provider facts have immutable DB triggers. Database-owner access still needs administrative discipline.
- Exactly one runtime worker, in-memory sign-in/provider limits and a shared STT/TTS semaphore bound demo use. Restarts reset counters; these are not account-wide durable spending limits.
- Body-free logs record generated request IDs, route templates, status and timing. Credentials/transcripts/audio do not belong in routine logs. No raw audio is stored as an application attachment.

Verification now includes 190 backend tests, strict lint/types, browser/accessibility evidence, dependency audits and a Linux Docker build gate. Dedicated XSS/injection, invalid/expired-token, injected transaction rollback, direct FK/check, permission-denial and microphone lifecycle regressions close the historical audit gaps. See [current verification](evidence/judge-readiness.md); this is not an exhaustive penetration-test claim.

Consenting test clips/raw responses remain in ignored `private/`; `.env`/private files are excluded from Docker context. Retain clips only through verification/submission review unless continued retention is consented. The UI discloses external Gnani processing and actual application retention; provider retention follows Gnani's own terms. Hosted Secure/HTTP-only/SameSite cookies, cross-origin mutation rejection, cross-worker denial, worker role restrictions and scoped bundle/log secret checks are evidenced in [hosted verification](evidence/hosted/README.md). The public JUDGE role is read-only, restricted to approved reports, denied billable endpoints and revoked when its flag is disabled.
