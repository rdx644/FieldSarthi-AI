# Gnani live integration evidence - WBS-01.6
**Status: NOT RUN / G1 NOT PASSED.** No authentic provider transcript/request ID is available yet.

Prerequisites: participant/account confirmation (G0), active scoped key with credits, consenting fresh synthetic-content Hindi recording. Root `.env` and `private/sample_hi.wav` are private and ignored.

Run the README cURL smoke first, then HTTPX adapter smoke. These are real requests, not tests with fixtures. A successful run creates `gnani-{transport}-{correlation}.json` here, with an actual provider-returned model and request ID, UTC timestamp, HTTP status, selected language, audio duration/SHA256 and transcript SHA256. Raw response transcript is retained only in ignored `private/` for operator review. Never paste credentials into this record.

Gate review checklist:
- [ ] G0 registration, eligibility, team and key/scope/credits confirmed
- [ ] Actual recorded Hindi audio metadata verified (WBS-01.1)
- [ ] Documented direct cURL request succeeded (WBS-01.2)
- [ ] Nonempty real transcript; genuine returned model/request ID/HTTP checked (WBS-01.3)
- [x] Typed real HTTPX adapter exists (WBS-01.4)
- [x] Required offline contract cases executed (WBS-01.5)
- [ ] Redacted actual evidence reviewed (WBS-01.6)
- [ ] Exact eventual deployment account/key confirmed; deployed re-smoke when deployment exists

Do not treat model/request values in unit fixtures or the source documentation as proof. No credential fingerprint is published. No deployment exists yet.
