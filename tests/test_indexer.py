from pathlib import Path

import pytest

from src.indexer import tokenize, build_index, save_index, load_index


def test_tokenize_lowercases_and_removes_punctuation():
    text = "Hello, WORLD! It's good."
    assert tokenize(text) == ["hello", "world", "it's", "good"]


def test_tokenize_handles_empty_text():
    assert tokenize("") == []


def test_build_index_stores_frequency_and_positions():
    pages = [
        {
            "url": "page1",
            "text": "good friends good"
        }
    ]

    index = build_index(pages)

    assert index["good"]["page1"]["frequency"] == 2
    assert index["good"]["page1"]["positions"] == [0, 2]
    assert index["friends"]["page1"]["frequency"] == 1
    assert index["friends"]["page1"]["positions"] == [1]


def test_build_index_handles_multiple_pages():
    pages = [
        {"url": "page1", "text": "life is good"},
        {"url": "page2", "text": "life is short"},
    ]

    index = build_index(pages)

    assert index["life"]["page1"]["frequency"] == 1
    assert index["life"]["page2"]["frequency"] == 1
    assert index["good"]["page1"]["positions"] == [2]
    assert index["short"]["page2"]["positions"] == [2]


def test_build_index_handles_empty_page_text():
    pages = [
        {"url": "page1", "text": ""}
    ]

    index = build_index(pages)

    assert index == {}


def test_save_and_load_index(tmp_path):
    index = {
        "life": {
            "page1": {
                "frequency": 2,
                "positions": [0, 3]
            }
        }
    }

    file_path = tmp_path / "index.json"

    save_index(index, file_path)
    loaded_index = load_index(file_path)

    assert loaded_index == index


def test_load_index_raises_error_for_missing_file(tmp_path):
    missing_file = tmp_path / "missing.json"

    with pytest.raises(FileNotFoundError):
        load_index(missing_file)