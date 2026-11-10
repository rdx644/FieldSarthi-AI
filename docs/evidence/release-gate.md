Latest temporary-demo engineering signoff — 2026-11-10

All identified engineering gaps are closed within the agreed scope. Application `85e1a5e20c1f623c0ce664493c8f002e7d5cff10`, engineering tag `demo-verified-2026-11-10`: 199 backend tests and required CI passed; actual hosted deploy -> compatible rollback -> restoration verified with all 12 persisted report details/audits/provenance and approved judge access unchanged. User provided actual-console credit observation; tested `GNANI_REQUESTS_ENABLED` pause controls both billable endpoints. No new recordings/provider calls. [Release proof](demo-operational-release.json).

Backups/December 9 expiry are user-managed for the temporary demo. Contributions/eligibility/video/post/form remain user-owned; Tamil excluded. Earlier remaining-gap notes below are historical and superseded by this record.

# Development release evidence - 2026-11-09 IST

Latest completion record: [judge readiness](judge-readiness.md), with 190 passing
backend tests and explicit closure of the earlier implementation/test gaps.
The following sections preserve historical checkpoints. Full participant submission
approval and free-plan backup limits remain separate. The genuine 15-recording results
(12/15; all safety cases blocked), ten genuine hosted workflows, public judge demo,
Timbre and restart checks are recorded in [current hosted proof](hosted/README.md).
Application commit `6f702c2` passed protected main CI and is deployed. Historical
pending observations below are superseded only where current evidence exists.

## Current full-roadmap audit
Actual hosting addendum: https://fieldsaarthi-ai.onrender.com is live under Blueprint GNANI. Real hosted prerecorded STT/TTS, browser supervisor workflow, production auth/secret boundaries and controlled restart persistence are verified in [hosted evidence](hosted/README.md). This supersedes the original missing-hosting observation below; a separate fresh human Hindi report is now verified below; authentic 15-clip evaluation and full-roadmap sign-off remain open.
The [complete audit](roadmap-audit.md) covers every numbered section/subsection and WBS task. Full roadmap sign-off is **HOLD**, with the 15-clip audio evaluation, ten-run reliability, dedicated negative-test, smaller implementation and managed-backup/rollback gaps still open. The candidate tag is not a final submission release. Exact merged-main `8146882` [CI passed](https://github.com/rdx644/FieldSarthi-AI/actions/runs/42527535002). Fresh local recheck: 87 tests passed in 21.97s, backend lint/format/types and frontend lint/format/type/build passed; root/live/ready HTTP 200 after restarting the existing private database/app. No fresh paid Gnani call was made during this audit.

## Fresh human microphone addendum
The participant reported recording a new Hindi microphone sentence on the hosted app and supplied WO-AFF1E3EE3BD2. Its 5.16-second audio metadata, nonempty raw transcript, genuine Prisma v2.5 request 0eb18653-4254-4502-8fe9-c774cd644693, confirmed intake, saved Warehouse C/Exhaust Fan C-03 order and creation audit were independently read back. The agent made no new provider request and left this user report OPEN. This is one participant-attested sample, not the 15-case evaluation, ten-run target or final public video.

## Verified locally
- Genuine cURL and HTTPX Prisma v2.5 calls: HTTP 200, actual returned model/request IDs and nonempty Hindi transcript. See gnani-stt-live.md.
- Full browser workflow: real prerecorded consenting voice upload -> actual Gnani -> human confirmation -> persisted order -> refresh -> supervisor assignment/start/resolution -> persisted audit. See browser/live-browser-smoke.json. This is not a claim of newly spoken microphone audio.
- MediaRecorder start/stop: verified with Chrome file-fed test audio and discarded without a second STT call.
- Timbre: real HTTP 200 binary WAV; repaired streaming header; actual 1.76-second PCM acknowledgment. Requested model timbre-v2.5; response does not echo a model ID. See gnani-tts-live.json.
- Backend: **87 tests passed**, including PostgreSQL races, idempotency, IDOR, role checks, immutability triggers, replay conflict precedence, CSRF, body limits and TTS failure isolation. Strict Ruff formatting/lint and mypy pass.
- Frontend: production TypeScript/Vite build, warning-free lint and formatting pass.
- Accessibility: six desktop/mobile axe WCAG2A/AA/2.1AA views, zero reported violations/JS errors/horizontal overflow. See browser/accessibility.json. This is automated coverage, not a universal accessibility certification.
- Text parser evaluation: 15/15 catalog fixtures pass; not an ASR accuracy metric. See ../tests/evaluation.csv.
- Backup/restore: actual pg_dump restored into a new scratch PostgreSQL DB, all seven table counts match, source unchanged. See backup-restore.json.
- Dependency audit: backend no known vulnerabilities; frontend npm audit zero reported vulnerabilities. Audit reports record executed scope; no claim of a penetration test.
- Cross-model review: reproduced and fixed all three identified boundary issues; reviewer found no actionable remaining violations in the corrected scope. See cross-model-review.md.
- One-page PDF pitch generated, page count checked and rendered for visual review.
- Render Blueprint static schema validation passes. Docker image build was executed successfully in GitHub CI; actual hosted execution is now verified separately below.

## External gates still requiring actual evidence
- [x] GitHub implementation published in PR #2; Linux quality/browser/audit/container build passed for application commit 0a6a3d8. [Executed run](https://github.com/rdx644/FieldSarthi-AI/actions/runs/42525267101). Any subsequent documentation-only commit remains subject to required current-head CI.
- [x] Protected main workflow enforced: required quality check, PR workflow, no force pushes/deletions. See github-publication.json.
- [x] Public HTTPS Render hosting, adopted Blueprint GNANI and deployed real-Gnani STT/TTS smoke with authorized key, using the existing consenting prerecorded sample; controlled restart preserves order/audit. See [hosted evidence](hosted/README.md).
- [ ] 15 distinct consenting authentic audio evaluation clips and reviewed ground truth.
- [x] Newly spoken Hindi microphone report supplied by participant as WO-AFF1E3EE3BD2; server provenance/durable creation independently inspected. Public video remains pending. See hosted/human-microphone-verification.json.

The user explicitly instructed: **do not submit the final form**. Contribution descriptions will be decided by the user. Registered emails are private. No social posting or final-form submission has been performed.

Local development completion does not claim production availability, official entry completion, CMMI certification, language recognition accuracy beyond the measured samples, or zero unknown vulnerabilities.

Additional development checks: real saved-ticket browser TTS decoded as a 6.4-second playable WAV (browser/live-tts-playback.json); network-body capture was unavailable so no body hash is invented. Keyboard skip-to-content preserves the current hash route and focuses main, covered by browser_quality.py. Fresh-clone private-directory and stale-credential export cases have explicit regression tests.

CI infrastructure findings were fixed without weakening application checks: Docker health-command quoting, checkout-name portability, fresh-clone private credential-directory creation, and stopping the browser test server before uv post-job cache pruning. The preceding Linux run passed all application/browser/audit/container stages; final commit-specific success must still be verified in the required GitHub quality check. Structured body-free HTTP logs now emit at INFO and propagate the HTTP request ID to Gnani, with a nonsecret telemetry regression test.
