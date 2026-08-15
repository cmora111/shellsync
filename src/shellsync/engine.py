from pathlib import Path
import shlex

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

                self._process_host_items(
                    remote,
                    host,
                    self._push_item,
                )

                self._push_system_hosts(remote)

        except (SSHError, SyncError) as exc:
            print(f"✗ ERROR: {exc}")
            return False

        return True

    def _status_system_hosts(
        self,
        remote: RemoteConnection,
    ) -> None:
        source = self.config.source_directory / "system" / "hosts"

        if not source.is_file():
            return

        destination = "/etc/hosts"

        local_hash = file_sha256(source)
        remote_hash = remote.file_hash(destination)

        if local_hash == remote_hash:
            print("  CURRENT     /etc/hosts")
        else:
            print("  UPDATE      /etc/hosts")

    def status_host(self, host: Host) -> bool:
        print(
            f"\nConnecting to {host.name} "
            f"({host.username}@{host.address})..."
        )

        try:
            with RemoteConnection(host) as remote:
                print(f"✓ Connected as {host.username}")

                self._process_host_items(
                    remote,
                    host,
                    self._status_item,
                )
                
                self._status_system_hosts(remote)

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

    def _process_host_items(
        self,
        remote: RemoteConnection,
        host: Host,
        processor,
    ) -> None:
        # Common files from sync.toml.
        for item in self.config.items:
            processor(remote, item)

        # Host-specific files.
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

            item = SyncItem(
                source=source,
                destination=f"{source.name}.{host.name}",
                recursive=False,
            )

            processor(remote, item)

    def _push_system_hosts(
        self,
        remote: RemoteConnection,
    ) -> None:
        source = self.config.source_directory / "system" / "hosts"

        if not source.is_file():
            return

        destination = "/etc/hosts"
        temp = remote.remote_path(".shellsync-hosts.tmp")

        local_hash = file_sha256(source)
        remote_hash = remote.file_hash(destination)

        if local_hash == remote_hash:
            print("  CURRENT     /etc/hosts")
            return

        if self.dry_run:
            print(f"  WOULD PUSH  {source} -> {destination}")
            return

        remote.upload_file(source, temp)

        status, _, stderr = remote.execute_sudo(
            "cp -a /etc/hosts /etc/hosts.sync-backup && "
            f"install -m 0644 {shlex.quote(temp)} /etc/hosts"
        )

        if status != 0:
            raise SyncError(
                f"Unable to install /etc/hosts: {stderr.strip()}"
            )

        new_hash = remote.file_hash(destination)

        if new_hash != local_hash:
            raise SyncError("Verification failed for /etc/hosts")

        remote.execute(f"rm -f -- {shlex.quote(temp)}")

        print("  PUSHED      /etc/hosts")
