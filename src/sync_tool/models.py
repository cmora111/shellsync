from dataclasses import dataclass
from pathlib import Path


@dataclass
class Host:
    name: str
    address: str
    username: str
    port: int = 22


@dataclass
class SyncItem:
    source: Path
    destination: str
    recursive: bool = False
