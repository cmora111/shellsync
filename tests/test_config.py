from pathlib import Path

import pytest

from shellsync.config import load_config


def test_load_config(tmp_path):
    config_file = tmp_path / "sync.toml"

    config_file.write_text(
        """
[settings]
source_directory = "files"
backup = true

[hosts.testhost]
address = "192.168.1.10"
username = "tester"

[[items]]
source = "common/.bashrc"
destination = ".bashrc"
"""
    )

    config = load_config(config_file)

    assert config.backup is True
    assert config.source_directory == tmp_path / "files"

    assert "testhost" in config.hosts

    host = config.hosts["testhost"]

    assert host.name == "testhost"
    assert host.address == "192.168.1.10"
    assert host.username == "tester"


def test_missing_config_file(tmp_path):
    missing = tmp_path / "does-not-exist.toml"


def test_source_directory_is_relative_to_config(tmp_path):
    config_file = tmp_path / "sync.toml"

    config_file.write_text(
        """
[settings]
source_directory = "files"

[hosts.testhost]
address = "localhost"
username = "tester"
"""
    )

    config = load_config(config_file)

    assert config.source_directory == tmp_path / "files"


def test_host_loaded_by_name(tmp_path):
    config_file = tmp_path / "sync.toml"

    config_file.write_text(
        """
[hosts.alienware]
address = "alienware"
username = "mora"
"""
    )

    config = load_config(config_file)

    assert "alienware" in config.hosts
    assert config.hosts["alienware"].name == "alienware"
