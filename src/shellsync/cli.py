from pathlib import Path
import argparse
import sys

from .config import load_config
from .engine import SyncEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sync",
        description=(
            "Synchronize shell configuration files "
            "to Linux hosts over SSH."
        ),
    )

    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        default=Path("sync.toml"),
        help="configuration file (default: sync.toml)",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    push = subparsers.add_parser(
        "push",
        help="push configuration to remote hosts",
    )

    push.add_argument(
        "hosts",
        nargs="*",
        help="hosts to update; default is all configured hosts",
    )

    push.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="show what would happen without copying anything",
    )

    subparsers.add_parser(
        "hosts",
        help="list configured hosts",
    )

    status_parser = subparsers.add_parser(
        "status",
        help="Show synchronization status",
    )

    status_parser.add_argument(
        "hosts",
        nargs="+",
    )

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        config = load_config(args.config)
    except (OSError, ValueError, KeyError) as exc:
        print(f"sync: configuration error: {exc}", file=sys.stderr)
        return 2

    if args.command == "hosts":
        for host in config.hosts.values():
            print(
                f"{host.name:<18} "
                f"{host.username}@{host.address}:{host.port}"
            )

        return 0

    if args.command == "push":
        if args.hosts:
            unknown = [
                name
                for name in args.hosts
                if name not in config.hosts
            ]

            if unknown:
                print(
                    "sync: unknown host(s): "
                    + ", ".join(unknown),
                    file=sys.stderr,
                )
                return 2

            hosts = [
                config.hosts[name]
                for name in args.hosts
            ]
        elif args.command == "status":
            engine = SyncEngine(config)

            ok = True

            for name in args.hosts:
                host = config.hosts[name]

                if not engine.status_host(host):
                    ok = False

            return 0 if ok else 1
        else:
            hosts = list(config.hosts.values())

        engine = SyncEngine(
            config,
            dry_run=args.dry_run,
        )

        success = True

        for host in hosts:
            if not engine.push_host(host):
                success = False

        return 0 if success else 1

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
