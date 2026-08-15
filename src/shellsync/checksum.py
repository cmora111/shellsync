from hashlib import sha256
from pathlib import Path


def file_sha256(path: Path) -> str:
    h = sha256()

    with path.open("rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)

    return h.hexdigest()
