from src.main import main


def test_main_load_print_find_and_exit(monkeypatch, capsys, tmp_path):
    test_index = {
        "good": {
            "page1": {"frequency": 2, "positions": [0, 2]}
        },
        "friends": {
            "page1": {"frequency": 1, "positions": [1]}
        }
    }

    commands = iter([
        "load",
        "print good",
        "find good friends",
        "exit"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(commands))
    monkeypatch.setattr("src.main.load_index", lambda: test_index)

    main()

    output = capsys.readouterr().out

    assert "Index loaded successfully." in output
    assert "page1" in output
    assert "score: 3" in output
    assert "Goodbye." in output


def test_main_handles_unknown_command(monkeypatch, capsys):
    commands = iter([
        "unknown",
        "exit"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(commands))

    main()

    output = capsys.readouterr().out

    assert "Unknown command." in output


def test_main_requires_index_before_search(monkeypatch, capsys):
    commands = iter([
        "find good",
        "print good",
        "exit"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(commands))

    main()

    output = capsys.readouterr().out

    assert "No index loaded. Run 'build' or 'load' first." in output