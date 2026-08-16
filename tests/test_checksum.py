from hashlib import sha256

from shellsync.checksum import file_sha256


def test_file_sha256(tmp_path):
    path = tmp_path / "example.txt"
    path.write_text("hello world")

    expected = sha256(b"hello world").hexdigest()

    assert file_sha256(path) == expected


def test_file_sha256_empty_file(tmp_path):
    path = tmp_path / "empty.txt"
    path.write_bytes(b"")

    expected = sha256(b"").hexdigest()

    assert file_sha256(path) == expected


def test_file_sha256_binary_file(tmp_path):
    path = tmp_path / "binary.dat"
    data = b"\x00\x01\x02\xff\xfe"

    path.write_bytes(data)

    assert file_sha256(path) == sha256(data).hexdigest()
