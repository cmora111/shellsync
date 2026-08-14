from __future__ import annotations

from pathlib import Path, PurePosixPath
import posixpath
import shlex
import stat

import paramiko

from .models import Host


class SSHError(RuntimeError):
    pass


class RemoteHost:
    def __init__(self, host: Host):
        self.host = host
        self.client: paramiko.SSHClient | None = None
        self.sftp: paramiko.SFTPClient | None = None
        self.home: str | None = None

    def __enter__(self) -> "RemoteHost":
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

    def connect(self) -> None:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.RejectPolicy())

        kwargs = {
            "hostname": self.host.address,
            "username": self.host.username,
            "port": self.host.port,
            "look_for_keys": True,
            "allow_agent": True,
        }

        if self.host.key_filename:
            kwargs["key_filename"] = str(self.host.key_filename)

        try:
            client.connect(**kwargs)
        except Exception as exc:
            client.close()
            raise SSHError(
                f"Unable to connect to {self.host.name}: {exc}"
            ) from exc

        self.client = client
        self.sftp = client.open_sftp()

        status, stdout, stderr = self.execute('printf "%s" "$HOME"')

        if status != 0:
            self.close()
            raise SSHError(
                f"Unable to determine home directory on "
                f"{self.host.name}: {stderr}"
            )

        self.home = stdout.strip()

    def close(self) -> None:
        if self.sftp is not None:
            self.sftp.close()
            self.sftp = None

        if self.client is not None:
            self.client.close()
            self.client = None

    def execute(self, command: str) -> tuple[int, str, str]:
        if self.client is None:
            raise SSHError("SSH connection is not open")

        _, stdout, stderr = self.client.exec_command(command)
        status = stdout.channel.recv_exit_status()

        return (
            status,
            stdout.read().decode("utf-8", errors="replace"),
            stderr.read().decode("utf-8", errors="replace"),
        )

    def remote_path(self, destination: str) -> str:
        if self.home is None:
            raise SSHError("Remote home directory is unknown")

        if destination.startswith("/"):
            return destination

        return posixpath.join(self.home, destination)

    def exists(self, path: str) -> bool:
        if self.sftp is None:
            raise SSHError("SFTP connection is not open")

        try:
            self.sftp.stat(path)
            return True
        except (FileNotFoundError, OSError):
            return False

    def mkdir_p(self, path: str) -> None:
        if self.sftp is None:
            raise SSHError("SFTP connection is not open")

        current = "/"

        for part in PurePosixPath(path).parts:
            if part == "/":
                continue

            current = posixpath.join(current, part)

            try:
                attrs = self.sftp.stat(current)

                if not stat.S_ISDIR(attrs.st_mode):
                    raise SSHError(
                        f"{current} exists but is not a directory"
                    )

            except FileNotFoundError:
                self.sftp.mkdir(current)

    def upload_file(self, source: Path, destination: str) -> None:
        if self.sftp is None:
            raise SSHError("SFTP connection is not open")

        parent = posixpath.dirname(destination)

        if parent:
            self.mkdir_p(parent)

        self.sftp.put(str(source), destination)

    def upload_directory(
        self,
        source: Path,
        destination: str,
    ) -> None:
        self.mkdir_p(destination)

        for child in source.iterdir():
            remote_child = posixpath.join(destination, child.name)

            if child.is_dir():
                self.upload_directory(child, remote_child)
            else:
                self.upload_file(child, remote_child)

    def backup(self, destination: str) -> str | None:
        if not self.exists(destination):
            return None

        backup_name = destination + ".sync-backup"

        command = (
            f"rm -rf -- {shlex.quote(backup_name)} && "
            f"cp -a -- {shlex.quote(destination)} "
            f"{shlex.quote(backup_name)}"
        )

        status, _, stderr = self.execute(command)

        if status != 0:
            raise SSHError(
                f"Backup failed for {destination}: {stderr.strip()}"
            )

        return backup_name
