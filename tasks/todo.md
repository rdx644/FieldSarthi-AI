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

See [current hosted evidence](../docs/evidence/improvement-hosted-release.json). Earlier checkpoints below retain their
historical scope and are superseded where they describe deployment/backup gates.

Current source completion - 2026-11-15: **specification engineering complete
and merged through protected PR #18**. Exact candidate and merged-application
main CI pass with 328 backend tests, 18 Chromium fixture accessibility/layout
views, dependency/static/build checks and the actual four-phase container
activation/rollback/restoration rehearsal. Read
[the source completion record](../docs/evidence/improvement-source-finalisation.json) for exact commits and CI links.

The accompanying maintenance change records the compatibility branch history
without changing any application file; its original deployable tip is preserved.
All future main updates continue through required CI and branch protection.
Production remains at `85e1a5e` with auto-deploy off, pending owner confirmation
of a current restore-ready backup and the staged release approval. Independent
held-out evaluation remains explicitly participant-deferred; no 95/100 result
is claimed. The earlier checkpoints below are historical and superseded for
source publication and local compatibility status.

Latest continuation ? 2026-11-15: **328 backend tests and 18 Chrome fixture
views pass; not deployed.** Follow-ups fix scarce-connection STT admission,
queue filter failure/retry, replay input protection, nested archive exclusions
and timeout cleanup. Strict checks and dependency audits pass. Fresh hosted
read-only checks preserve the sole approved sample, original transcript hash,
OPEN/version-1 state and one audit event. The hosted app remains `85e1a5e`.
See [current follow-up verification](../docs/evidence/improvement-continuation-verification.json). Exact follow-up CI and protected
source merge are next; production remains gated on owner backup confirmation.
Earlier checkpoint records below retain their historical scope.

Latest ownership update: production backup is handled by the participant and
completion is not yet confirmed. The agent completes automatic source publication,
protected merge, CI and local/main synchronization. Engineering and image rollback
are verified; live migration waits for backup confirmation. See
[current status](../docs/release-finalisation.md). Earlier checkpoint statements below retain their scope.

Latest finalisation: **307 backend tests and actual container compatibility,
rollback and restoration pass locally**; independent evaluation is explicitly
participant-deferred. The prepared compatibility build resolves the earlier local
blocker. Both source CI runs pass; approved production backup/deployment remains pending.
See [current finalisation](../docs/release-finalisation.md). Earlier checkpoint statements below retain their
historical scope.

Latest improvement verification ? 2026-11-15: **295 backend tests and 16 Chrome
fixture accessibility/layout views pass locally. Not deployed.** All 34 T-IMP IDs
are accounted for in [the improvement checklist](improvements.md); exact candidate
CI, compatibility/backup/deployment and independent live evaluation remain gated.
See [the current handoff](../docs/improvement-handoff.md). No new provider calls,
recordings, production writes or participant submissions.

Current improvement work — 2026-11-14: see [the separate improvement checklist](improvements.md).
The November 10 signoff below is historical. New code is locally verified only;
production migration/deployment, independent audio evaluation and participant
submission remain gated as recorded in that checklist.

Latest temporary-demo engineering signoff — 2026-11-10

All identified engineering gaps are closed within the agreed scope. Application `85e1a5e20c1f623c0ce664493c8f002e7d5cff10`, engineering tag `demo-verified-2026-11-10`: 199 backend tests and required CI passed; actual hosted deploy -> compatible rollback -> restoration verified with all 12 persisted report details/audits/provenance and approved judge access unchanged. User provided actual-console credit observation; tested `GNANI_REQUESTS_ENABLED` pause controls both billable endpoints. No new recordings/provider calls. [Release proof](../docs/evidence/demo-operational-release.json).

Backups/December 9 expiry are user-managed for the temporary demo. Contributions/eligibility/video/post/form remain user-owned; Tamil excluded. Earlier remaining-gap notes below are historical and superseded by this record.

# Latest scoped roadmap review ? 2026-11-10

- [x] Downloads roadmap hash verified; 24 sections / 94 headings / 64 WBS tasks individually mapped in docs/evidence/end-to-end-roadmap-audit.json.
- [x] Three ASR failure corrections verified by cached-transcript replay in isolated tests; original automatic 12/15 score retained.
- [x] 193 backend tests, strict backend/frontend and complete fixture browser/accessibility checks.
- [x] Existing branch commits already included in main; publish audit via protected PR.
- User-reserved: contributions/eligibility/video/post/form. Tamil excluded by user.
- Production exceptions: managed backups/free DB expiry, actual app rollback rehearsal, operator credit monitoring and final submission tag/signoff. See docs/final-project-context.md.

# Execution status

## Judge-ready implementation update

- [x] FR-04..12: distinct MANUAL_TEXT path, immutable source/provenance, actionable
  provider errors, disclosure, parser version/exact source spans and conservative ambiguity handling.
- [x] FR-20..25: priority/location/assignee controls, audited cancellation reason,
  typed responses and explicitly approved read-only public judge dashboard.
- [x] NFR-01/03/04/09: ten consecutive controlled API workflows; missing atomicity,
  same-key race, required-field, failed-intake, token, duplicate, readiness, WebM,
  TTS, correction immutability and stage-telemetry regression cases.
- [x] 190 backend tests; frontend build/lint/format; six retained and ten new
  browser accessibility/layout checks, permission-denied/XSS/complete workflow.
- [x] Full reachable Git history/index scan, automatic CI browser workflow,
  fresh private local backup/isolated restore, independent review and mutation check.
- [x] Authentic 15-recording manifest, resumable genuine-provider runner, recording
  guide and judge walkthrough prepared. All 15 participant clips are captured privately.
- [x] Genuine 15-recording evaluation: 12/15 complete cases, all six safety cases
  blocked; Hindi/English/Hinglish development corpus, English substitutions for
  04/10, Tamil unverified, initial failures and same-corpus refinement disclosed.
- [x] Protected PR #8, exact application-main CI and live deployment at 6f702c2.
- [x] Ten consecutive genuine hosted voice-to-resolved workflows, separate genuine
  Timbre WAV, deployed judge desktop/mobile checks and controlled restart persistence.
- [ ] Participant eligibility/contributions, final video/public post/release review;
  final official form remains explicitly reserved for the user.

See [current evidence](../docs/evidence/judge-readiness.md). Earlier checklists below
retain their historical test counts; this update supersedes those implementation gaps.

Full audit on 2026-11-09: [all 94 numbered headings and 64 WBS tasks](../docs/evidence/roadmap-audit.md). That historical audit identified implementation/test/evaluation gaps now addressed by the current completion record. Participant submission gates and free-host managed-backup limitations remain open. Earlier development checkmarks retain their original scope.
## WBS-00: Compliance and configuration
- [x] Official rules/docs checked, P0 baseline frozen, original roadmap/source evidence preserved.
- [x] Genuine key/STT access verified; user reports 5,000 starting credits and permits the same key for hosting.
- [x] User confirms team of two, registration and final-form receipt; names/institution received.
- [ ] Each member's individual eligibility/registration attestation and final contribution descriptions remain user-owned.
- [x] GitHub implementation published in PR #2 and protected main verified.
- [x] Remaining deployment/audio acceptance work tracked in GitHub issues #3 and #4.
- [x] Application commit 0a6a3d8 passed Linux/browser/audit/container CI; protected PR merges also require the current head to be green.
## WBS-01: Real Gnani spike
- [x] WBS-01.1 through WBS-01.6: actual WAV validated, direct cURL + backend HTTPX real responses, tests and sanitized evidence.
- [x] Exact deployed-account/key genuine STT and optional TTS smoke verified on Render with consenting prerecorded sample; docs/evidence/hosted/.
## WBS-02: Foundation
- [x] React/Vite/TypeScript and typed FastAPI; real PostgreSQL 18; versioned Alembic schema.
- [x] Seven domain tables, synthetic two-worker/supervisor seed, salted Argon2 authentication and live role checks.
- [x] Health/readiness, strict same-origin cookies/CSRF/CORS, typed errors and correlation logs; DB/access tests.
## WBS-03: Audio/intake
- [x] Recorder permission handling, 25-second stop, preview/rerecord and upload alternatives.
- [x] Before-parser size cap, bounded real FFmpeg decoding/normalization, actual sample-count duration check.
- [x] Real Prisma adapter, preserved raw transcript/provenance and READY_FOR_REVIEW intake only after genuine success.
- [x] Temporary cleanup and corrupt/long/no-speech/provider failure tests.
- [x] Participant-attested fresh Hindi HTTPS microphone report WO-AFF1E3EE3BD2 verified by read-back of confirmed intake, actual Prisma provenance and durable creation audit; final public demo video remains pending.
## WBS-04: Reviewed work orders
- [x] Unicode aliases, location/asset relationship, issue/urgency evidence, unknown-field blocking.
- [x] Corrected transcript separate from raw, strict explicit confirmation, server-generated IDs.
- [x] Atomic intake/order/audit/idempotency transaction, unique intake barrier, same/different-key replay conflicts and concurrency tests.
- [x] Refresh persistence and 15/15 measured text parser fixtures; negative validation.
## WBS-05: Supervisor
- [x] Authorized paged queue/search/status filters, assignment, priority and permitted transitions.
- [x] Version conflicts, atomic immutable events, details/original/corrected transcript and chronological audit.
- [x] Real browser assignment -> in progress -> resolution and refresh verified.
## WBS-06: Optional polish
- [x] Genuine Timbre WAV verified; bounded binary adapter repairs streaming length; saved-ticket-only playback.
- [x] TTS outage leaves order/audit unchanged, tested.
- [x] Ownership-safe duplicate warnings and responsive/empty/error/accessibility polish.
- [x] Model/language limitations documented honestly.
## WBS-07: Release
- [x] 87 backend tests, strict lint/format/type, frontend build/lint/format, six axe/mobile/browser views.
- [x] RBAC/IDOR, provider and media failures, idempotency/version conflicts, secret boundaries and dependency audit.
- [x] Actual private backup/isolated restore drill with matching table counts.
- [x] Docker/Render/CI configuration and static Render schema validation.
- [x] Remote Linux/browser/audit/container build and protected main enforcement verified; see github-publication.json.
- [x] Render CLI authorized; free web/PostgreSQL18 resources live; actual Blueprint GNANI in_sync; real hosted prerecorded STT/TTS and restart persistence verified.
- [x] Separate participant-attested fresh Hindi HTTPS microphone report verified with actual distinct Gnani request and saved order; no 15-case or multilingual accuracy claim.
- [x] 15 distinct participant recordings evaluated with genuine Prisma: 12/15 complete cases; all six safety cases blocked. See current evidence for limitations.
## WBS-08: User-owned submission
- [x] One-page PDF/Markdown pitch, accurate project explanation, 2-3 minute script and social draft prepared.
- [ ] Final working video/public post/actual individual contribution statements.
- [ ] User will submit the form later; **agent must not submit it**.

All actual evidence is in docs/evidence/. No production, public-post or official-form completion is claimed without proof.
