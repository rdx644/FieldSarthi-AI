# Development release evidence - 2026-11-09 IST
## Verified locally
- Genuine cURL and HTTPX Prisma v2.5 calls: HTTP 200, actual returned model/request IDs and nonempty Hindi transcript. See gnani-stt-live.md.
- Full browser workflow: real prerecorded consenting voice upload -> actual Gnani -> human confirmation -> persisted order -> refresh -> supervisor assignment/start/resolution -> persisted audit. See browser/live-browser-smoke.json. This is not a claim of newly spoken microphone audio.
- MediaRecorder start/stop: verified with Chrome file-fed test audio and discarded without a second STT call.
- Timbre: real HTTP 200 binary WAV; repaired streaming header; actual 1.76-second PCM acknowledgment. Requested model timbre-v2.5; response does not echo a model ID. See gnani-tts-live.json.
- Backend: **83 tests passed**, including PostgreSQL races, idempotency, IDOR, role checks, immutability triggers, replay conflict precedence, CSRF, body limits and TTS failure isolation. Strict Ruff formatting/lint and mypy pass.
- Frontend: production TypeScript/Vite build, warning-free lint and formatting pass.
- Accessibility: six desktop/mobile axe WCAG2A/AA/2.1AA views, zero reported violations/JS errors/horizontal overflow. See browser/accessibility.json. This is automated coverage, not a universal accessibility certification.
- Text parser evaluation: 15/15 catalog fixtures pass; not an ASR accuracy metric. See ../tests/evaluation.csv.
- Backup/restore: actual pg_dump restored into a new scratch PostgreSQL DB, all seven table counts match, source unchanged. See backup-restore.json.
- Dependency audit: backend no known vulnerabilities; frontend npm audit zero reported vulnerabilities. Audit reports record executed scope; no claim of a penetration test.
- Cross-model review: reproduced and fixed all three identified boundary issues; reviewer found no actionable remaining violations in the corrected scope. See cross-model-review.md.
- One-page PDF pitch generated, page count checked and rendered for visual review.
- Render Blueprint static schema validation passes. Docker image execution and remote CI are tracked separately below.

## External gates still requiring actual evidence
- [ ] GitHub published branch/PR and remote CI/container build outcome recorded.
- [ ] Protected main workflow enforcement verified.
- [ ] Public HTTPS hosting and deployed real-Gnani smoke with the authorized key.
- [ ] 15 distinct consenting authentic audio evaluation clips and reviewed ground truth.
- [ ] Newly spoken human microphone sentence in the final demonstration.

The user explicitly instructed: **do not submit the final form**. Contribution descriptions will be decided by the user. Registered emails are private. No social posting or final-form submission has been performed.

Local development completion does not claim production availability, official entry completion, CMMI certification, language recognition accuracy beyond the measured samples, or zero unknown vulnerabilities.
