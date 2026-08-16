import shellsync.output as output


def test_success(capsys, monkeypatch):
    monkeypatch.setattr(output, "USE_COLOR", False)

    output.success("Connected as tester")

    captured = capsys.readouterr()

    assert captured.out == "✓ Connected as tester\n"


def test_error(capsys, monkeypatch):
    monkeypatch.setattr(output, "USE_COLOR", False)

    output.error("Connection failed")

    captured = capsys.readouterr()

    assert captured.err == "✗ Connection failed\n"


def test_heading(capsys, monkeypatch):
    monkeypatch.setattr(output, "USE_COLOR", False)

    output.heading("Connecting to testhost...")

    captured = capsys.readouterr()

    assert "Connecting to testhost..." in captured.out


def test_current_status(capsys, monkeypatch):
    monkeypatch.setattr(output, "USE_COLOR", False)

    output.print_status("CURRENT", ".bash_aliases")

    captured = capsys.readouterr()

    assert "CURRENT" in captured.out
    assert ".bash_aliases" in captured.out


def test_update_status(capsys, monkeypatch):
    monkeypatch.setattr(output, "USE_COLOR", False)

    output.print_status("UPDATE", ".bashrc")

    captured = capsys.readouterr()

    assert "UPDATE" in captured.out
    assert ".bashrc" in captured.out


def test_status_color_mapping(capsys, monkeypatch):
    monkeypatch.setattr(output, "USE_COLOR", True)

    output.print_status("CURRENT", ".bashrc")
    output.print_status("UPDATE", ".profile")
    output.print_status("MISSING", ".missing")

    captured = capsys.readouterr()

    assert "\033[32m" in captured.out
    assert "\033[33m" in captured.out
    assert "\033[31m" in captured.out
