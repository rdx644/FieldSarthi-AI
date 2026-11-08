# WBS-01 integration boundaries
Applying security-and-hardening skill to already authorized Gnani integration.
Assets: server-only API key, consented voice, transcript, credits and truthful evidence.
Boundaries: local audio -> validation; environment -> credential header; external HTTPS provider -> strict response schema; response -> private/public evidence split.
Controls: fixed official endpoint, TLS defaults, redirects disabled, no secret in cURL argv/errors, 10 MiB local cap, strict PCM smoke metadata, 25s cap, response cap, explicit live consent and spend flags, bounded retries/timeouts, ignored private files.
No HTTP upload endpoint/auth/database/UI is introduced in this phase. Callers of the bytes adapter must perform audio validation; the smoke runner does. Later ffmpeg conversion/RBAC are tracked in the roadmap.
Retain local voice/raw response only through live verification and submission review; remove private recordings after review unless explicit continued consent. No raw audio in Git or public evidence. Provider retention settings and production privacy obligations require later review; no production privacy compliance claim.
