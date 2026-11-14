# Security and source distribution — IMP-00

The three shared synthetic demo account logins in [README](../README.md#demo-access)
are intentionally public by participant authorization on November 10, 2026.
Worker and supervisor activity is shared with other users of those accounts;
this temporary demo is not private or a production access model. Their publication
does not authorize disclosure of Gnani keys, database credentials, JWT secrets,
hosting tokens, private account exports or raw recordings. Changing published
access or rotating credentials remains an owner decision.

The password-free judge session is read-only and exposes only explicitly approved
synthetic evidence. Publication authorization covers **WO-AFF1E3EE3BD2**; it does
not extend to other reports or recordings. Do not add new judge-visible reports
without participant approval and consent review.

## Distributing source safely

Ignore rules apply to Git and Docker, not to a recursive ZIP of the workspace.
Private runtime files, backups and audio must remain local. Distribute the public
repository or export a reviewed, verified commit from the **repository root**:

```powershell
git rev-parse HEAD
git archive --format=zip --output=output/fieldsaarthi-source.zip <verified-commit>
api/.venv/Scripts/python.exe api/scripts/repository_guard.py --archive output/fieldsaarthi-source.zip
```

Create the ignored `output` directory first on a fresh clone. On other platforms,
use `uv run python` from `api/` to run the guard with the archive's absolute path.
The ZIP contains committed source only; uncommitted improvements need their own
reviewed commit before export. Do not recursively archive the working directory
and do not distribute a ZIP just because a previous ZIP appeared safe.

The archive guard reads member names and bounded contents without extraction. It
rejects private/environment/media/backup/runtime artifacts, nested archives,
private graph/reference exports, traversal, symlinks and known key signatures.
Migration SQL and sanitized JSON evidence remain allowed. Inspection limits are
10,000 members, 100 MiB expanded total and 10 MiB per file. An archive exceeding
these limits needs explicit review rather than bypassing checks. No secret body
is printed on rejection.

The regular guard scans reachable Git history and the index for prohibited paths
and known signatures:

```powershell
cd api
uv run python scripts/repository_guard.py
```

Passing these deterministic checks does not establish that all credentials are
absent, that every document is approved for publication, or that historical
copies held elsewhere are safe. If an actual credential exposure is found, stop
distribution and notify the owner without printing the value. Credential rotation
and history remediation require owner authorization; do not rewrite Git history.

## Provider and infrastructure controls

Judge access cannot initiate paid speech. Manual text is a distinct workflow.
The owner monitors the actual provider console balance; application admission
counters do not measure money. Use `GNANI_REQUESTS_ENABLED=false` to pause both
speech endpoints; applying a Render environment change requires deployment.
Maintain single-worker deployment and the documented backup/expiry procedures in
[operations](operations.md). The historically recorded free database expiry is
December 9, 2026; current retention and expiry require operator verification.
