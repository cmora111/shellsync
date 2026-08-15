from pathlib import Path

from .models import Config, Host, SyncItem
from .remote import RemoteConnection, SSHError, SyncError
from .checksum import file_sha256

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
        print(
            f"\nConnecting to {host.name} "
            f"({host.username}@{host.address})..."
        )

        try:
            with RemoteConnection(host) as remote:
                print(f"✓ Connected as {host.username}")

                # Push common files defined in sync.toml.
                for item in self.config.items:
                    self._push_item(remote, item)

                # Push host-specific files automatically.
                self._push_host_files(remote, host)

        except (SSHError, SyncError) as exc:
            print(f"✗ ERROR: {exc}")
            return False

        return True

    def status_host(self, host: Host) -> bool:
        print(
            f"\nConnecting to {host.name} "
            f"({host.username}@{host.address})..."
        )

        try:
            with RemoteConnection(host) as remote:
                print(f"✓ Connected as {host.username}")

                for item in self.config.items:
                    self._status_item(remote, item)

                self._status_host_files(remote, host)

        except (SSHError, SyncError) as exc:
            print(f"✗ ERROR: {exc}")
            return False

        return True

    def _status_item(
        self,
        remote: RemoteConnection,
        item: SyncItem,
    ) -> None:
        source = item.source
        destination = remote.remote_path(item.destination)

        if not source.exists():
            print(f"  MISSING     {item.destination}")
            return

        local_hash = file_sha256(source)
        remote_hash = remote.file_hash(destination)

        if local_hash == remote_hash:
            print(f"  CURRENT     {item.destination}")
        else:
            print(f"  UPDATE      {item.destination}")

    def _push_host_files(
        self,
        remote: RemoteConnection,
        host: Host,
    ) -> None:
        host_directory = (
            self.config.source_directory
            / "hosts"
            / host.name
        )

        if not host_directory.is_dir():
            return

        for source in sorted(host_directory.iterdir()):
            if not source.is_file():
                continue

            # Keep the host suffix on the remote side.
            #
            # Example:
            #
            # files/hosts/r400/.bash_aliases
            #     -> ~/.bash_aliases.r400
            #
            # files/hosts/r400/.bash_local
            #     -> ~/.bash_local.r400
            destination = f"{source.name}.{host.name}"

            item = SyncItem(
                source=source,
                destination=destination,
                recursive=False,
            )

            self._push_item(remote, item)

    def _status_host_files(
        self,
        remote: RemoteConnection,
        host: Host,
    ) -> None:
        host_directory = (
            self.config.source_directory
            / "hosts"
            / host.name
        )

        if not host_directory.is_dir():
            return

        for source in sorted(host_directory.iterdir()):
            if not source.is_file():
                continue

            destination = f"{source.name}.{host.name}"

            item = SyncItem(
                source=source,
                destination=destination,
                recursive=False,
            )

            self._status_item(remote, item)

    def _push_item(
        self,
        remote: RemoteConnection,
        item: SyncItem,
    ) -> None:

        source = item.source
        destination = remote.remote_path(item.destination)

        if not source.exists():
            print(f"  MISSING     {source}")
            return

        # New code starts here
        local_hash = file_sha256(source)
        remote_hash = remote.file_hash(destination)

        if local_hash == remote_hash:
            print(f"  CURRENT     {item.destination}")
            return
        else:
            print(f"  UPDATE      {item.destination}")

        if self.dry_run:
            print(
                f"  WOULD PUSH  {source} -> {destination}"
            )
            return

        if self.config.backup and remote.exists(destination):
            backup = remote.backup(destination)
            if backup:
                print(f"  BACKUP      {destination}")

        if source.is_dir():
            remote.upload_directory(source, destination)
        else:
            remote.upload_file(source, destination)

        # Verify the upload.
        new_hash = remote.file_hash(destination)

        if new_hash != local_hash:
            raise SyncError(
                f"Verification failed for {destination}"
            )

        print(f"  PUSHED      {item.destination}")
