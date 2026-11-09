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
