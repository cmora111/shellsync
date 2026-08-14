from pathlib import Path
import tomllib

from .models import Config, Host, SyncItem


def load_config(path: Path) -> Config:
    with path.open("rb") as fp:
        raw = tomllib.load(fp)

    settings = raw.get("settings", {})

    source_directory = Path(
        settings.get("source_directory", "files")
    )

    if not source_directory.is_absolute():
        source_directory = path.parent / source_directory

    hosts: dict[str, Host] = {}

    for name, values in raw.get("hosts", {}).items():
        key_filename = values.get("key_filename")

        hosts[name] = Host(
            name=name,
            address=values.get("address", name),
            username=values["username"],
            port=values.get("port", 22),
            key_filename=(
                Path(key_filename).expanduser()
                if key_filename
                else None
            ),
        )

    items: list[SyncItem] = []

    for values in raw.get("items", []):
        items.append(
            SyncItem(
                source=source_directory / values["source"],
                destination=values["destination"],
                recursive=values.get("recursive", False),
            )
        )

    return Config(
        source_directory=source_directory,
        backup=settings.get("backup", True),
        hosts=hosts,
        items=items,
    )
