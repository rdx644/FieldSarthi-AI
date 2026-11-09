"""NFR-04/05: scan all reachable Git history for private paths, raw media and key signatures.

No content/secret values are printed. This deterministic guard complements review;
it is not a claim to detect every possible credential format.
"""

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MEDIA = {
    ".wav",
    ".mp3",
    ".webm",
    ".m4a",
    ".ogg",
    ".flac",
    ".mp4",
    ".mov",
    ".aac",
    ".dump",
    ".pem",
    ".p12",
}
SIGNATURES = [
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(rb"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    re.compile(rb"\bgithub_pat_[A-Za-z0-9_]{40,}\b"),
    re.compile(rb"\bAKIA[0-9A-Z]{16}\b"),
]
ASSIGNMENT = re.compile(
    rb"(?im)^[ \t]*(?:export[ \t]+)?"
    rb"(?:GNANI_API_KEY_ID|JWT_SECRET|DEMO_(?:WORKER2?|SUPERVISOR)_PASSWORD)"
    rb"[ \t]*=[ \t]*[\"']?([^\r\n\"']*)"
)


def forbidden_path(path):
    parts = Path(path.replace("\\", "/")).parts
    name = parts[-1] if parts else ""
    return (
        "private" in parts
        or name == ".env"
        or (name.startswith(".env.") and name != ".env.example")
        or Path(name).suffix.lower() in MEDIA
    )


def inspect_content(body):
    if any(pattern.search(body) for pattern in SIGNATURES):
        return True
    for match in ASSIGNMENT.finditer(body):
        value = match.group(1).strip()
        if value.startswith((b"os.environ[", b"os.getenv(")):
            continue
        if value and not any(
            marker in value.upper()
            for marker in [
                b"REPLACE",
                b"YOUR",
                b"CHANGE",
                b"CI_",
                b"CI-",
                b"TEST",
                b"EXAMPLE",
                b"${",
            ]
        ):
            return True
    return False


def git(*arguments, data=None):
    return subprocess.run(
        ["git", *arguments], input=data, capture_output=True, check=True, cwd=ROOT
    ).stdout


def historical_paths():
    # Blob enumeration deduplicates identical bytes under different filenames.
    raw = git("log", "--all", "--full-history", "-m", "--format=", "--name-only", "-z")
    return {path.strip("\n") for path in raw.decode().split("\0") if path.strip("\n")}


def main():
    objects = git("rev-list", "--objects", "--all").decode().splitlines()
    index = git("ls-files", "--stage").decode().splitlines()
    objects.extend(line.split()[1] + " " + line.split("\t", 1)[1] for line in index)
    paths = {}
    failures = []
    for path in historical_paths():
        if forbidden_path(path):
            failures.append("Forbidden historical path: " + path)
    for line in objects:
        oid, _, path = line.partition(" ")
        if path:
            paths[oid] = path
            if forbidden_path(path):
                failures.append("Forbidden historical path: " + path)
    ids = "\n".join(paths) + "\n"
    metadata = git("cat-file", "--batch-check=%(objectname) %(objecttype)", data=ids.encode())
    blobs = [line.split()[0] for line in metadata.decode().splitlines() if line.endswith(" blob")]
    stream = git("cat-file", "--batch", data=("\n".join(blobs) + "\n").encode())
    offset = 0
    for oid in blobs:
        stop = stream.index(b"\n", offset)
        size = int(stream[offset:stop].split()[-1])
        content = stream[stop + 1 : stop + 1 + size]
        if inspect_content(content):
            failures.append(
                "Credential signature in historical blob " + oid[:12] + ": " + paths[oid]
            )
        offset = stop + 1 + size + 1
    for failure in failures:
        print(failure)
    if failures:
        raise SystemExit(1)
    print(
        f"Repository guard passed: {len(blobs)} historical blobs; "
        "no forbidden paths/media/key signatures."
    )


if __name__ == "__main__":
    main()
