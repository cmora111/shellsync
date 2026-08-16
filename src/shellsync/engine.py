from pathlib import Path
import shlex

from .models import Config, Host, SyncItem
from .remote import RemoteConnection, SSHError, SyncError
from .checksum import file_sha256
from .output import ( 
    heading,
    success,
    error,
    print_status,
)

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
        heading(
            f"Connecting to {host.name} "
            f"({host.username}@{host.address})..."
        )

        try:
            with RemoteConnection(host) as remote:
                success(f"Connected as {host.username}")

                self._process_host_items(
                    remote,
                    host,
                    self._push_item,
                )

                self._push_system_hosts(remote)

        except (SSHError, SyncError) as exc:
            error("ERROR:", str(exc))
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
            print_status("CURRENT", destination)
        else:
            print_status("UPDATE", destination)
    def status_host(self, host: Host) -> bool:
        heading(
            f"Connecting to {host.name} "
            f"({host.username}@{host.address})..."
        )

        try:
            with RemoteConnection(host) as remote:
                success(f"Connected as {host.username}")

                self._process_host_items(
                    remote,
                    host,
                    self._status_item,
                )
                
                self._status_system_hosts(remote)

        except (SSHError, SyncError) as exc:
            error("ERROR:", str(exc))
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
            print_status("MISSING", item.destination)
            return

        local_hash = file_sha256(source)
        remote_hash = remote.file_hash(destination)

        if local_hash == remote_hash:
            print_status("CURRENT", item.destination)
        else:
           print_status("UPDATE", item.destination)

    def _push_item(
        self,
        remote: RemoteConnection,
        item: SyncItem,
    ) -> None:

        source = item.source
        destination = remote.remote_path(item.destination)

        if not source.exists():
            print_status("MISSING", source)
            return

        # New code starts here
        local_hash = file_sha256(source)
        remote_hash = remote.file_hash(destination)

        if local_hash == remote_hash:
            print_status("CURRENT", item.destination)
            return

        if self.dry_run:
            print_status(
                "WOULD PUSH", f"{source} -> {destination}"
            )
            return

        if self.config.backup and remote.exists(destination):
            backup = remote.backup(destination)
            if backup:
                print_status("BACKUP", destination)

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

        print_status("PUSHED", item.destination)

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
        destination = "/etc/hosts"
        backup = f"{destination}.sync-backup"

        source = self.config.source_directory / "system" / "hosts"

        if not source.is_file():
            return

        temp = remote.remote_path(".shellsync-hosts.tmp")

        local_hash = file_sha256(source)
        remote_hash = remote.file_hash(destination)

        if local_hash == remote_hash:
            print_status("CURRENT", destination) 
            return

        if self.dry_run:
            print_status("WOULD PUSH", f"{source} -> {destination}")
            return

        remote.upload_file(source, temp)

        exit_status, _, stderr = remote.execute_sudo(
            f"cp -a {shlex.quote(destination)} {shlex.quote(backup)} && "
            f"install -m 0644 {shlex.quote(temp)} {shlex.quote(destination)}"
        )

        if exit_status != 0:
            raise SyncError(
                f"Unable to install {destination}: {stderr.strip()}"
            )

        new_hash = remote.file_hash(destination)

        if new_hash != local_hash:
            raise SyncError(f"Verification failed for {destination}: {stderr.strip()}")

        remote.execute(f"rm -f -- {shlex.quote(temp)}")

        print_status("PUSHED", destination)

