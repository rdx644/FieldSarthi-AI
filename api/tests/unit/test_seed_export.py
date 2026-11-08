import json

from app.seed import write_accounts


def test_fresh_clone_creates_private_credential_directory(tmp_path):
    accounts = [{"email": "fixture@example.test", "password": "fixture-not-a-real-password"}]
    write_accounts(accounts, root=tmp_path)
    assert json.loads((tmp_path / "private/demo-accounts.json").read_text()) == accounts


def test_reseed_replaces_stale_credential_for_same_identity(tmp_path):
    write_accounts([{"email": "fixture@example.test", "password": "old-fixture"}], root=tmp_path)
    write_accounts([{"email": "fixture@example.test", "password": "new-fixture"}], root=tmp_path)
    saved = json.loads((tmp_path / "private/demo-accounts.json").read_text())
    assert len(saved) == 1 and saved[0]["password"] == "new-fixture"
