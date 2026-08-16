# shellsync

Synchronize shell configuration files across Linux hosts over SSH.

`shellsync` keeps your dotfiles synchronized using SHA-256 checksums,
only transferring files that have changed. It supports common files,
host-specific files, and selected system files such as `/etc/hosts`.

---

## Features

- SSH/SFTP-based synchronization
- SHA-256 checksum comparison
- Dry-run mode
- Status reporting
- Automatic backups
- Host-specific configuration
- System file synchronization
- Upload verification

---

## Installation

```bash
git clone ...
cd shellsync

python -m venv .venv
source .venv/bin/activate
pip install -e .
```

---

## Project Layout

```
shellsync/
├── files/
│   ├── common/
│   ├── hosts/
│   │   ├── alienware/
│   │   └── r400/
│   └── system/
│       └── hosts
├── sync.toml
└── src/
```

---

## Configuration

Example `sync.toml`:

```toml
source_directory = "files"
backup = true

[[hosts]]
name = "alienware"
address = "alienware"
username = "mora"

[[hosts]]
name = "r400"
address = "192.168.1.119"
username = "pi"

[[items]]
source = "common/.bash_aliases"
destination = ".bash_aliases"

[[items]]
source = "common/.bash_functions"
destination = ".bash_functions"
```

---

## Usage

Check synchronization status:

```bash
sync status alienware
```

Preview changes:

```bash
sync push alienware --dry-run
```

Synchronize files:

```bash
sync push alienware
```

Synchronize multiple hosts:

```bash
sync push alienware r400
```

---

## Host-specific files

Files placed in:

```
files/hosts/<hostname>/
```

are uploaded as:

```
.<filename>.<hostname>
```

Example:

```
files/hosts/r400/.bash_aliases
```

becomes:

```
~/.bash_aliases.r400
```

---

## System files

Currently supported:

- `/etc/hosts`

System files are:

- compared using SHA-256
- uploaded via `sudo`
- backed up before replacement
- verified after installation

---

## Typical workflow

```bash
sync status r400
sync push r400 --dry-run
sync push r400
sync status r400
```

---

## Exit codes

| Code | Meaning |
|-----:|---------|
| 0 | Success |
| 1 | Synchronization completed with errors |
| 2 | Invalid command or configuration |


---

## Requirements

- Python 3.11+
- OpenSSH server
- `sha256sum`
- Passwordless SSH authentication (recommended)
- Passwordless `sudo` for managed system files

---

## Roadmap

Planned features:

- `sync doctor`
- Improved diagnostics
- Automated test suite
- Additional managed system files

---

## License

MIT

---

## Philosophy

`shellsync` is intentionally small.

It is designed to manage personal shell configuration across a handful 
of trusted Linux systems. Rather than trying to replace configuration 
management frameworks, it emphasizes simplicity, safety, and predictable 
behavior.
