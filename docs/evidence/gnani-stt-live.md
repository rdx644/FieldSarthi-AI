# Genuine Gnani Prisma live verification - WBS-01
**Local integration spike PASSED on 2026-11-08.** Two actual outbound requests used the private user-provided verification credential. No fixture or synthesized transcript was used.

User confirmed registration, team of two, receipt of final form and 5,000 available credits. Balance is user-reported; the authenticated console balance was not independently queried, and remaining balance after these calls is unknown.

Input: user-prepared `private/sample_hi.wav`, actual 11.9580625-second mono PCM16 16kHz WAV, 382702 bytes. The user replied ready after recording/consent instructions. Audio SHA256: `558b1916693e824cb3be9f3104ff94035c518a5895499872bba5b55a3e2ca4e5`. Selected language `hi-IN`; requested and returned model `prisma-v2.5`; HTTPS POST to official `/stt/v3`.

| Transport | HTTP | Returned model | Actual returned request ID | Sanitized evidence |
|---|---|---|---|---|
| curl | 200 | prisma-v2.5 | fc53ad95-3121-446f-9ee2-b7ac2e4d5503 | [gnani-curl-fc53ad95-3121-446f-9ee2-b7ac2e4d5503.json](gnani-curl-fc53ad95-3121-446f-9ee2-b7ac2e4d5503.json) |
| httpx | 200 | prisma-v2.5 | 5da963a4-4279-4527-9461-d487feca6250 | [gnani-httpx-5da963a4-4279-4527-9461-d487feca6250.json](gnani-httpx-5da963a4-4279-4527-9461-d487feca6250.json) |

Actual commands from api/:
```powershell
uv run python -m app.integrations.smoke ..\private\sample_hi.wav --live --synthetic-consented --transport curl
uv run python -m app.integrations.smoke ..\private\sample_hi.wav --live --synthetic-consented --transport httpx
```
Both commands exited 0. Exactly two live requests were issued; retries were disabled. HTTPX measured elapsed time: 2.4696556 seconds. Both returned the same nonempty transcript, reviewed for the intended synthetic water-pump fault scenario. Neither reported truncation. Transcript SHA256: `c583c43b345f95a0fc504ce6212ef793d807ad9c6bc5dd16e6298cca4e64db91`. The verbatim transcript and original recording remain private; public evidence contains no credential or raw transcript/audio.

- [x] WBS-01.1 actual recorded Hindi audio metadata verified
- [x] WBS-01.2 real direct cURL request succeeds
- [x] WBS-01.3 nonempty transcript and actual model/request ID/HTTP verified
- [x] WBS-01.4 real HTTPX adapter succeeds with the same key/audio
- [x] WBS-01.5 41 offline tests passed in the preceding code verification; no code changed for these live calls
- [x] WBS-01.6 sanitized actual evidence saved and checked against private transcript/audio hashes

**Gate interpretation:** the local Gnani integration spike is proved. The user described this credential as for verification. No deployment exists and no assertion is made that it is the eventual deployed account/key. The roadmap's strict release requirement for the exact deployed credential remains pending a deployed re-smoke. Participant eligibility attestations and remote GitHub/protected-main setup remain separately tracked WBS-00 items.
