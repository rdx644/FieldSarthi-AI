# ADR-009: Explicitly approved read-only public judge access

Status: accepted by the user in the 2026-11-09 completion session.

Judges need a direct dashboard entry without receiving team passwords. Add a
JUDGE role and password-free session endpoint, controlled by
PUBLIC_JUDGE_DEMO_ENABLED. Publish only orders with judge_visible=true. The user
explicitly approved transcript/audit publication for WO-AFF1E3EE3BD2; the migration
allows that one existing synthetic report and defaults every other report to false.

All reads enforce the role and publication allowlist, including direct intake IDs
and duplicate suggestions. All mutations and billable audio calls deny JUDGE.
Disabling the flag revokes existing judge sessions at authentication time.
Accounts and team passwords remain private. Publication is not a replacement for
the genuine worker/supervisor flow or the participant's final video.

Rollback to pre-JUDGE code requires first deactivating every JUDGE user: historical
queue authorization does not recognize this role. See the operations runbook.
