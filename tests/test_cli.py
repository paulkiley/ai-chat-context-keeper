from chat_history_manager import cli
from chat_history_manager.utils import read_chat_index


def test_cli_save_and_retrieve(temp_history_dir, stdin_text, capsys):
    stdin_text("CLI content test")
    rc = cli.main(
        [
            "save",
            "--project-name",
            "PX",
            "--topic",
            "TX",
            "--summary",
            "CLI Sum",
        ]
    )
    assert rc == 0

    # Retrieve
    rc = cli.main(
        [
            "retrieve",
            "--project-name",
            "PX",
            "--topic",
            "TX",
            "--limit",
            "1",
        ]
    )
    assert rc == 0
    out = capsys.readouterr().out
    assert "CLI content test" in out


def test_cli_dry_run(temp_history_dir, stdin_text):
    # Dry-run should not create files or index
    stdin_text("DRYRUN")
    rc = cli.main(
        [
            "save",
            "--project-name",
            "PX",
            "--topic",
            "TX",
            "--summary",
            "CLI Sum",
            "--dry-run",
        ]
    )
    assert rc == 0
    # index remains empty
    assert read_chat_index() == []


def test_cli_read_only_blocks_write(temp_history_dir, stdin_text, monkeypatch, capsys):
    monkeypatch.setenv("CHM_READ_ONLY", "1")
    stdin_text("RO")
    rc = cli.main(
        [
            "save",
            "--project-name",
            "PX",
            "--topic",
            "TX",
        ]
    )
    assert rc != 0
    err = capsys.readouterr().err
    assert "Read-only" in err
