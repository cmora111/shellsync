from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Host:
    name: str
    address: str
    username: str
    port: int = 22
    key_filename: Path | None = None


@dataclass(frozen=True)
class SyncItem:
    source: Path
    destination: str
    recursive: bool = False


@dataclass(frozen=True)
class Config:
    source_directory: Path
    backup: bool
    hosts: dict[str, Host]
    items: list[SyncItem]
