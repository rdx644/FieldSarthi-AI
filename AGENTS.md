# FieldSaarthi agent rules
Read tasks/todo.md, docs/rtm.md and docs/evidence/judge-readiness.md first. Reference FR/NFR/O IDs.
For repository architecture or implementation work, use docs/architecture.md, docs/final-project-context.md, docs/rtm.md and actual tracked source. Optional graphify-out exports are private local aids, ignored by Git and excluded from Docker; they are not required for a fresh clone. Do not publish them or make public documentation depend on them. Any private graph refresh must use git ls-files inputs and exclude private data, credentials, raw audio and untracked paths.
Scope: user authorized engineering completion and repository cleanup on 2026-11-09.
The original implementation roadmap and docs/submission drafts are deliberately excluded from Git at the user's request. Ignored local copies may exist; use them for reference but do not republish them.
User explicitly approved public read-only transcript/audit publication of WO-AFF1E3EE3BD2. Other reports remain private by default. Final contributions and the official submission form remain user-owned.
Keep infrastructure credentials in private .env; audio and raw live responses in private/. On 2026-11-10 the user explicitly authorized publishing the three shared synthetic demo account logins in README.md. Only those demo login values are public; Gnani keys, database credentials and JWT secrets remain private. Shared worker/supervisor access does not change the restricted public judge allowlist.
Never fake a provider response outside tests or invent request/model metadata.
Never mark gates passed without actual evidence. Record exact executed checks.
