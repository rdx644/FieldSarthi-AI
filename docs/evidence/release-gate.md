# Development release evidence - 2026-11-09 IST
## Current full-roadmap audit
The [complete audit](roadmap-audit.md) covers every numbered section/subsection and WBS task. Full roadmap sign-off is **HOLD**, with human speech/evaluation, actual hosting/restart, dedicated negative-test and smaller implementation gaps still open. The candidate tag is not a final submission release. Exact merged-main `8146882` [CI passed](https://github.com/rdx644/FieldSarthi-AI/actions/runs/42527535002). Fresh local recheck: 87 tests passed in 21.97s, backend lint/format/types and frontend lint/format/type/build passed; root/live/ready HTTP 200 after restarting the existing private database/app. No fresh paid Gnani call was made during this audit.

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
- Render Blueprint static schema validation passes. Docker image build was executed successfully in GitHub CI; actual hosted execution remains a separate gate below.

## External gates still requiring actual evidence
- [x] GitHub implementation published in PR #2; Linux quality/browser/audit/container build passed for application commit 0a6a3d8. [Executed run](https://github.com/rdx644/FieldSarthi-AI/actions/runs/42525267101). Any subsequent documentation-only commit remains subject to required current-head CI.
- [x] Protected main workflow enforced: required quality check, PR workflow, no force pushes/deletions. See github-publication.json.
- [ ] Public HTTPS hosting and deployed real-Gnani smoke with the authorized key.
- [ ] 15 distinct consenting authentic audio evaluation clips and reviewed ground truth.
- [ ] Newly spoken human microphone sentence in the final demonstration.

The user explicitly instructed: **do not submit the final form**. Contribution descriptions will be decided by the user. Registered emails are private. No social posting or final-form submission has been performed.

Local development completion does not claim production availability, official entry completion, CMMI certification, language recognition accuracy beyond the measured samples, or zero unknown vulnerabilities.

Additional development checks: real saved-ticket browser TTS decoded as a 6.4-second playable WAV (browser/live-tts-playback.json); network-body capture was unavailable so no body hash is invented. Keyboard skip-to-content preserves the current hash route and focuses main, covered by browser_quality.py. Fresh-clone private-directory and stale-credential export cases have explicit regression tests.

CI infrastructure findings were fixed without weakening application checks: Docker health-command quoting, checkout-name portability, fresh-clone private credential-directory creation, and stopping the browser test server before uv post-job cache pruning. The preceding Linux run passed all application/browser/audit/container stages; final commit-specific success must still be verified in the required GitHub quality check. Structured body-free HTTP logs now emit at INFO and propagate the HTTP request ID to Gnani, with a nonsecret telemetry regression test.
