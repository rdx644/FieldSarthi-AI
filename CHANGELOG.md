## Unreleased — targeted engineering improvements, 2026-11-15

Local candidate only; migration/deployment and independent speech evaluation remain gated.

- Add role-scoped SQL queue summaries that retain correct totals across pages and filters.
- Clarify read-only judge navigation, human confirmation, language readiness and location/equipment review.
- Guard tracked source ZIPs and compressed backups; add network-free WER/CER scoring with explicit denominators and private-input preservation, including hard links.
- Add a durable shared STT/TTS admission ledger and serialize concurrent login throttle checks.
- Preserve rules-v4 and original provider facts; verify cached safety/correction regressions.
- Record 295 backend tests, 16 Chrome fixture views and a full requirement handoff. No provider calls or production changes; previous-image compatibility at schema 0005 blocks rollout.

## Demo operational controls ? 2026-11-10

- Operators can pause both live STT and TTS with `GNANI_REQUESTS_ENABLED=false`; manual reports and saved workflows stay available.
- Added regression coverage for pause isolation and shared hourly request limits. Actual account credits remain console-monitored; no automatic monetary limit is claimed.

# Changelog

## Unreleased — judge evaluation candidate

### Added
- Password-free read-only judge dashboard for explicitly approved demonstration reports.
- Accessible typed reporting with clear manual provenance and human confirmation.
- Exact transcript evidence spans/parser versions and conservative multiple-asset handling.
- Priority/location/assignee queue controls and required audited cancellation reasons.
- Resumable authentic-recording evaluation and genuine hosted reliability tools.

### Fixed
- Judge sessions revoke immediately when public access is disabled.
- Navigating between order details resets stale order/action state.
- Provider errors give actionable recovery guidance; no false successful report.
- Readiness checks the exact migration heads, not only database connectivity.

### Verification
- Expanded backend, transactional, provider/media, browser, privacy and CI history gates.
- Genuine recording scores, participant contributions/video/post and final submission
  remain evidence requirements; no final submission release is declared here.
