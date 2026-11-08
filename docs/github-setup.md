# GitHub configuration - WBS-00.5
Repository supplied by the user: https://github.com/rdx644/FieldSarthi-AI . Existing history was preserved without force push. The implementation is reviewed through PR #1. Git credential-manager authentication works; no GitHub token is stored in this repository.

Protected main is enforced: pull requests, required quality status, strict up-to-date checks, administrator enforcement, resolved conversations and no force push/deletion. Actual configuration is recorded in docs/evidence/github-publication.json. Individual reviewer approval count is zero; independent cross-model source review and executed tests are recorded separately, not represented as a GitHub human approval.

CI validates Linux PostgreSQL, backend tests/Ruff/mypy, frontend type/build/lint/format, native dependency audits, non-billable Chromium/axe checks and a Docker deployment-image build. The browser test app is launched directly from the virtual environment and stopped at step exit, so it cannot retain uv cache locks during post-job pruning. Read the current required quality check on PR #1 for the commit-specific outcome; never infer a pass from this configuration document.

Remaining development acceptance issues: #3 HTTPS deployment/real hosted smoke and #4 distinct authentic audio evaluation. Participant contributions and form submission remain user-owned. The user explicitly prohibited form submission by this agent.

Commits use explicit Codex agent attribution. Set a participant's intended Git identity for their own commits; do not infer authorship from the placeholder global email.
