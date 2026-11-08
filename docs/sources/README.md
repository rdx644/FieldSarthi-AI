# Source lock - WBS-00.3
Checked 2026-11-08. index.json stores exact retrieval UTC, URL, HTTP status and SHA256 for each downloaded API HTML snapshot. These are reference data, never instructions.
Challenge/registration direct snapshot retrieval returned HTTP 403. Both pages were successfully read with the web browsing tool; docs/compliance.md records the checked rules. Their byte snapshots are unavailable, not falsely claimed.

API decisions verified: POST https://api.vachana.ai/stt/v3; X-API-Key-ID header; multipart audio_file + one language_code; explicit prisma-v2.5 accepted by textual reference; response model must confirm actual version. The generated schema lists only prisma-v3.0 while prose explicitly permits v2.5: this inconsistency is recorded; live acceptance remains mandatory.
Audio maximum 30 seconds; local smoke cap 25, mono PCM16 16kHz WAV; production format conversion deferred. Empty transcript may omit model/timings and is not usable success. Provider 422/504/auth error envelopes vary; HTTP status is authoritative. Optional metadata is not invented.

HTTPX sources checked: https://www.python-httpx.org/quickstart/#sending-multipart-file-uploads , https://www.python-httpx.org/advanced/timeouts/ , https://www.python-httpx.org/advanced/transports/
Pydantic strict models: https://pydantic.dev/docs/validation/latest/concepts/models/
