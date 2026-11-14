import pytest

from scripts.repository_guard import forbidden_path, inspect_content


@pytest.mark.parametrize(
    "path",
    [".env", "private/record.json", "api/.env.local", "clip.m4a", "old/clip.wav", "backup.dump"],
)
def test_private_paths_and_raw_media_are_blocked(path):
    assert forbidden_path(path)


@pytest.mark.parametrize(
    "path",
    [
        ".env.example",
        "docs/evidence/proof.json",
        "web/src/pages/Report.tsx",
        "docs/submission/solution-pitch.pdf",
    ],
)
def test_reviewable_artifacts_are_allowed(path):
    assert not forbidden_path(path)


def test_key_signatures_and_nonplaceholder_assignments_are_blocked():
    assert inspect_content(("ghp_" + "A" * 36).encode())
    assert inspect_content(b"GNANI_API_KEY_ID=actual-random-value")
    assert not inspect_content(b"GNANI_API_KEY_ID=REPLACE_IN_PRIVATE_ENV_ONLY")
    assert not inspect_content(b'JWT_SECRET = os.environ["JWT_SECRET"]')


@pytest.mark.parametrize(
    "path",
    [
        "backups/database.sql",
        "database-backup.sql",
        "snapshot.sql.gz",
        "database.dump.gz",
        "snapshot.sql.zst",
        "database.dump.zstd",
        "workspace.tar.xz",
        "workspace.tar.bz2",
        "workspace.tar.zst",
        "workspace.txz",
        "workspace.tbz2",
        "workspace.tzst",
        "Gnani.zip",
        "workspace.tar.gz",
        "runtime/worker.pid",
        "local/PGDATA/PG_VERSION",
        "local/postmaster.opts",
        "local/pg_hba.conf",
        "private-exports/accounts.json",
        "PRIVATE/record.json",
    ],
)
def test_imp_002_backup_archive_and_runtime_paths_are_blocked(path):
    assert forbidden_path(path)


@pytest.mark.parametrize(
    "path",
    [
        "api/alembic/versions/0005.sql",
        "docs/examples/schema.sql",
        "api/scripts/backup_drill.py",
        "docs/evidence/backup-restore.json",
        "docs/evidence/hosted/runtime-verification.json",
    ],
)
def test_imp_002_legitimate_sql_tools_and_sanitized_evidence_are_allowed(path):
    assert not forbidden_path(path)


def test_imp_001_archive_checks_paths_and_contents_without_disclosing_secrets(tmp_path, capsys):
    import zipfile

    from scripts.repository_guard import inspect_archive

    archive = tmp_path / "source.zip"
    secret = "ghp_" + "A" * 36
    with zipfile.ZipFile(archive, "w") as target:
        target.writestr("safe.txt", "source only")
        target.writestr("private/accounts.json", "private")
        target.writestr("../escape.txt", "outside")
        target.writestr("settings.txt", secret)
    count, failures = inspect_archive(archive)
    assert count == 4
    assert len(failures) == 3
    assert secret not in " ".join(failures)
    assert secret not in capsys.readouterr().out


def test_imp_001_clean_archive_is_allowed(tmp_path):
    import zipfile

    from scripts.repository_guard import inspect_archive

    archive = tmp_path / "source.zip"
    with zipfile.ZipFile(archive, "w") as target:
        target.writestr(".env.example", "GNANI_API_KEY_ID=REPLACE_PRIVATE_ENV")
        target.writestr("api/alembic/versions/0005.sql", "SELECT 1;")
        target.writestr("docs/evidence/proof.json", "{}")
    assert inspect_archive(archive) == (3, [])


@pytest.mark.parametrize(
    "name",
    [
        "DOCS/SUBMISSION/draft.md",
        "Docs/Roadmap.md",
        "fieldsaarthi_ai_traceable_implementation_roadmap.md",
    ],
)
def test_imp_001_private_reference_export_exclusions_ignore_case(tmp_path, name):
    import zipfile

    from scripts.repository_guard import inspect_archive

    archive = tmp_path / "source.zip"
    with zipfile.ZipFile(archive, "w") as target:
        target.writestr(name, "private reference")
    count, failures = inspect_archive(archive)
    assert count == 1
    assert len(failures) == 1


def test_imp_001_archive_rejects_links_runtime_and_oversized_members(tmp_path):
    import stat
    import zipfile

    from scripts.repository_guard import inspect_archive

    archive = tmp_path / "source.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as target:
        link = zipfile.ZipInfo("link.txt")
        link.create_system = 3
        link.external_attr = (stat.S_IFLNK | 0o777) << 16
        target.writestr(link, "private/accounts.json")
        target.writestr(".git/config", "runtime")
        target.writestr("graphify-out/context.json", "private reference")
        target.writestr("large.txt", b"0" * (10 * 1024 * 1024 + 1))
    count, failures = inspect_archive(archive)
    assert count == 4
    assert len(failures) == 4


def test_deleted_forbidden_path_with_identical_safe_blob_is_still_found(tmp_path, monkeypatch):
    import subprocess

    from scripts import repository_guard

    monkeypatch.setattr(repository_guard, "ROOT", tmp_path)

    def git(*args):
        subprocess.run(
            ["git", "-c", "user.name=Guard Test", "-c", "user.email=guard@example.test", *args],
            cwd=tmp_path,
            check=True,
            capture_output=True,
        )

    git("init", "--quiet")
    (tmp_path / "safe.txt").write_text("same harmless bytes")
    git("add", "safe.txt")
    git("commit", "-qm", "Add safe file")
    (tmp_path / ".env").write_text("same harmless bytes")
    git("add", "-f", ".env")
    git("commit", "-qm", "Add forbidden historical path")
    git("rm", ".env")
    git("commit", "-qm", "Remove forbidden path")
    assert ".env" in repository_guard.historical_paths()
    with pytest.raises(SystemExit):
        repository_guard.main()
