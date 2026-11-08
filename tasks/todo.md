# Execution tracker
## WBS-00 - G0 pending
- [ ] WBS-00.1: Official rules read; user confirmed registration, team of two and form receipt; individual eligibility and both-member registration confirmation remain. Evidence: docs/compliance.md.
- [x] WBS-00.2: Private verification key configured; STT scope proved by two actual HTTP 200 responses; user reports 5,000 available credits. Current console balance not independently queried.
- [x] WBS-00.3: Official sources checked; API snapshots/hashes and challenge retrieval limitations recorded in docs/sources/.
- [x] WBS-00.4: Title, P0 scope, roles, Hindi baseline, scenario frozen in docs/scope.md.
- [ ] WBS-00.5: Local Git, CI, issue template, RTM and risks prepared. Local baseline saved with Codex agent attribution; remote repo and protected main pending GitHub/account setup.
## WBS-01 - local live spike passed; deployed-credential release check pending
- [x] WBS-01.1: User-prepared real Hindi WAV verified: mono PCM16, 16kHz, 11.958 seconds.
- [x] WBS-01.2: Genuine direct cURL call succeeded, HTTP 200; sanitized evidence saved.
- [x] WBS-01.3: Authentic nonempty transcript, prisma-v2.5, returned request IDs and HTTP 200 verified for both transports.
- [x] WBS-01.4: GnaniSpeechClient HTTPX adapter implemented; see api/app/integrations/gnani.py.
- [x] WBS-01.5: Required success/no-speech/400/401/402/403/429/500/timeout cases pass offline.
- [x] WBS-01.6: Actual sanitized cURL/HTTPX evidence saved; hashes checked against private original audio/transcripts.
## Checkpoint
- [ ] G0 participant/account verified
- [x] Local G1 spike: authentic cURL + backend proof verified with verification credential
- [ ] Strict release G1: exact eventual deployed account/key re-smoke pending deployment
- [ ] Remote workflow/protection verified
WBS-02 onward remains unstarted in this execution. Local integration proof exists; exact deployed-credential verification remains mandatory before release.
