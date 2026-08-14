from .models import Config, Host, SyncItem
from .remote import RemoteConnection, SSHError


class SyncEngine:
    def __init__(
        self,
        config: Config,
        *,
        dry_run: bool = False,
    ):
        self.config = config
        self.dry_run = dry_run

    def push_host(self, host: Host) -> bool:
        print(f"\nConnecting to {host.name} ({host.username}@{host.address})...")

        try:
            with RemoteConnection(host) as remote:
                print(f"✓ Connected as {host.username}")

                for item in self.config.items:
                    self._push_item(remote, item)

        except SSHError as exc:
            print(f"  ERROR: {exc}")
            return False

        return True

    def _push_item(
        self,
        remote: RemoteConnection,
        item: SyncItem,
    ) -> None:
        source = item.source
        destination = remote.remote_path(item.destination)

        if not source.exists():
            print(f"  MISSING  {source}")
            return

        if source.is_dir() and not item.recursive:
            print(
                f"  SKIP     {source.name} "
                "(directory not marked recursive)"
            )
            return

        if self.dry_run:
            print(f"  WOULD PUSH  {source} -> {destination}")
            return

        if self.config.backup and remote.exists(destination):
            backup = remote.backup(destination)

            if backup:
                print(f"  BACKUP   {destination} -> {backup}")

        if source.is_dir():
            remote.upload_directory(source, destination)
        else:
            remote.upload_file(source, destination)

        print(f"  PUSHED   {source.name}")
