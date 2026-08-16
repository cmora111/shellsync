from shellsync.remote import SSHError, SyncError


def test_ssh_error_is_exception():
    error = SSHError("connection failed")

    assert isinstance(error, Exception)
    assert str(error) == "connection failed"


def test_sync_error_is_exception():
    error = SyncError("sync failed")

    assert isinstance(error, Exception)
    assert str(error) == "sync failed"
