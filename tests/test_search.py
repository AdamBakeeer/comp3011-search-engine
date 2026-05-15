from src.search import print_word, find_query


def sample_index():
    return {
        "good": {
            "page1": {"frequency": 2, "positions": [0, 2]},
            "page2": {"frequency": 1, "positions": [4]},
        },
        "friends": {
            "page1": {"frequency": 1, "positions": [1]},
            "page3": {"frequency": 1, "positions": [5]},
        },
        "life": {
            "page2": {"frequency": 3, "positions": [1, 7, 9]},
        },
    }


def test_print_word_returns_index_entry():
    index = sample_index()

    result = print_word(index, "good")

    assert result == index["good"]


def test_print_word_is_case_insensitive():
    index = sample_index()

    result = print_word(index, "GOOD")

    assert result == index["good"]


def test_print_word_returns_none_for_missing_word():
    index = sample_index()

    result = print_word(index, "missing")

    assert result is None


def test_print_word_returns_none_for_empty_input():
    index = sample_index()

    result = print_word(index, "")

    assert result is None


def test_find_query_single_word_returns_ranked_results():
    index = sample_index()

    results = find_query(index, "good")

    assert results == [
        {"url": "page1", "score": 2},
        {"url": "page2", "score": 1},
    ]


def test_find_query_multi_word_uses_and_logic():
    index = sample_index()

    results = find_query(index, "good friends")

    assert results == [
        {"url": "page1", "score": 3}
    ]


def test_find_query_is_case_insensitive():
    index = sample_index()

    results = find_query(index, "GOOD FRIENDS")

    assert results == [
        {"url": "page1", "score": 3}
    ]


def test_find_query_empty_query_returns_empty_list():
    index = sample_index()

    assert find_query(index, "") == []


def test_find_query_missing_word_returns_empty_list():
    index = sample_index()

    assert find_query(index, "nonsense") == []


def test_find_query_requires_all_terms_to_match():
    index = sample_index()

    results = find_query(index, "friends life")

    assert results == []

def test_find_query_handles_punctuation():
    index = sample_index()

    results = find_query(index, "good, friends!")

    assert results == [
        {"url": "page1", "score": 3}
    ]

def test_find_query_handles_extra_spaces():
    index = sample_index()

    results = find_query(index, "   good   friends   ")

    assert results == [
        {"url": "page1", "score": 3}
    ]