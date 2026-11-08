# Final-form project explanation
**Title:** FieldSaarthi AI - Multilingual Voice-to-Action Intelligence for Field Operations.
**Team:** Shubham Putitundi; Shambhavi Kumar.
**Problem/users:** Field maintenance workers need to turn informal spoken faults into clear, accountable work for supervisors and technicians.
**Working solution:** A short Hindi/Hinglish recording is transcribed by the real Gnani Prisma API. Catalog-backed suggestions are shown beside the unmodified transcript. Human confirmation creates exactly one persisted work order. Supervisors assign, prioritize and progress it through controlled states, with immutable provenance/audit history and an optional genuine Gnani Timbre spoken acknowledgment.
**Models actually verified:** Prisma v2.5 returned in live STT responses; Timbre v2.5 requested in successful binary-WAV calls. No claim of Prisma v3 or autonomous asset recognition by Gnani.
**Technologies:** React, TypeScript, Vite, FastAPI, Pydantic, SQLAlchemy, Alembic, PostgreSQL, HTTPX, FFmpeg, Pytest and Playwright. Hosting artifacts: Docker and Render Blueprint.
**Evidence:** docs/evidence/gnani-stt-live.md; docs/evidence/browser/live-browser-smoke.json; docs/evidence/gnani-tts-live.json; docs/evidence/browser/accessibility.json; docs/evidence/backup-restore.json.
**Limitations:** Synthetic inventory; selected-language short clips; Hindi speech baseline; the recorded automated browser proof reuses a consenting voice sample and is not a claim of fresh human speech. Real English/Tamil speech evaluation, 15 distinct authentic audio cases, public-host smoke and official submission remain separately tracked.
**Contributions:** Confirm actual responsibilities for both participants before final submission. AI-assisted implementation/testing was used; do not invent either participant's code ownership.
**Public demo/post URL:** Pending publication, never fabricate a URL.
