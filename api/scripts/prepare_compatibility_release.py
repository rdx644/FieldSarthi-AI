"""Export a reviewed, speech-paused rollback build; never deploy or change a DB.

Run from api: python -m scripts.prepare_compatibility_release --output ../output/bridge-source
The output must not already exist. The baseline is deliberately fixed and verified
against the previous deployed app, not taken from arbitrary untracked workspace files.
"""

import argparse
import hashlib
import json
import subprocess
import tempfile
import zipfile
from pathlib import Path

from scripts.repository_guard import inspect_archive

ROOT = Path(__file__).resolve().parents[2]
BASELINE = "0fca9716e3589eb9cac70f12e2468aacf7cadb5a"
PREVIOUS_APPLICATION = "85e1a5e20c1f623c0ce664493c8f002e7d5cff10"
MIGRATION = "api/alembic/versions/0005_provider_admissions.py"


def git(*arguments):
    return subprocess.check_output(["git", *arguments], cwd=ROOT, timeout=30)


def replace_once(path, original, replacement):
    body = path.read_text(encoding="utf-8")
    if body.count(original) != 1:
        raise ValueError("Previous-source layout changed; compatibility patch needs review.")
    path.write_text(body.replace(original, replacement), encoding="utf-8", newline="\n")


def prepare_release(output):
    output = Path(output).resolve()
    if output.exists():
        raise FileExistsError("Preserve the existing output; select a new directory.")
    for source_path in (
        "api/app",
        "web/src",
        "api/scripts/start.py",
        "Dockerfile",
        "api/uv.lock",
        "web/package-lock.json",
        "api/alembic",
        "api/alembic.ini",
    ):
        if git("rev-parse", BASELINE + ":" + source_path) != git(
            "rev-parse", PREVIOUS_APPLICATION + ":" + source_path
        ):
            raise ValueError("Baseline is not the verified previous application source.")
    with tempfile.TemporaryDirectory(prefix="fieldsaarthi-bridge-") as temporary:
        archive = Path(temporary) / "source.zip"
        archive.write_bytes(git("archive", "--format=zip", BASELINE))
        _, failures = inspect_archive(archive)
        if failures:
            raise ValueError("Previous source export failed the publication guard.")
        output.mkdir(parents=True)
        with zipfile.ZipFile(archive) as bundle:
            bundle.extractall(output)
    # Exact known revisions only. No arbitrary future schema is treated as ready.
    replace_once(
        output / "api/app/main.py",
        "if versions != schema_heads:",
        'if versions not in ({"0004"}, {"0005"}):',
    )
    replace_once(
        output / "api/scripts/start.py",
        'subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"], check=True)',
        'os.environ["GNANI_REQUESTS_ENABLED"] = "false"\n'
        'subprocess.run([sys.executable, "-m", "scripts.schema_bridge"], check=True)',
    )
    replace_once(
        output / "Dockerfile",
        "COPY api/scripts/start.py ./scripts/start.py",
        "COPY api/scripts/start.py ./scripts/start.py\n"
        "COPY api/scripts/schema_bridge.py ./scripts/schema_bridge.py",
    )
    for name in (MIGRATION, "api/scripts/schema_bridge.py"):
        (output / name).write_bytes((ROOT / name).read_bytes())
    changed_files = [
        "api/app/main.py",
        "api/scripts/start.py",
        "Dockerfile",
        "api/scripts/schema_bridge.py",
        MIGRATION,
    ]
    manifest = {
        "profile": "previous-application-schema-bridge-speech-paused",
        "source_baseline": BASELINE,
        "previous_application": PREVIOUS_APPLICATION,
        "previous_app_source_identical": True,
        "preparation_source_sha": git("rev-parse", "HEAD").decode().strip(),
        "accepted_schema_heads": ["0004", "0005"],
        "automatic_migration": False,
        "billable_speech": "forced paused before startup validation and serving",
        "changed_files": changed_files,
        "changed_file_sha256": {
            name: hashlib.sha256((output / name).read_bytes()).hexdigest() for name in changed_files
        },
        "deployment": "not performed; operator approval, exact CI and backup required",
    }
    (output / "compatibility-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        prepare_release(args.output)
    except Exception:
        parser.exit(2, "Compatibility export failed; check source identity and output path.\n")
    print("Compatibility source prepared; no provider call, deployment or database change.")


if __name__ == "__main__":
    main()
