from src.search import (
    print_word,
    find_query,
    get_total_documents,
    calculate_tfidf_score,
    suggest_terms,
)


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


def test_get_total_documents_counts_unique_pages():
    index = sample_index()

    assert get_total_documents(index) == 3


def test_calculate_tfidf_score_increases_with_frequency():
    index = sample_index()
    total_documents = get_total_documents(index)

    page1_score = calculate_tfidf_score(index, "good", "page1", total_documents)
    page2_score = calculate_tfidf_score(index, "good", "page2", total_documents)

    assert page1_score > page2_score


def test_find_query_single_word_returns_ranked_results():
    index = sample_index()

    results = find_query(index, "good")

    assert len(results) == 2
    assert results[0]["url"] == "page1"
    assert results[1]["url"] == "page2"
    assert results[0]["score"] > results[1]["score"]


def test_find_query_multi_word_uses_and_logic():
    index = sample_index()

    results = find_query(index, "good friends")

    assert len(results) == 1
    assert results[0]["url"] == "page1"


def test_find_query_is_case_insensitive():
    index = sample_index()

    results = find_query(index, "GOOD FRIENDS")

    assert len(results) == 1
    assert results[0]["url"] == "page1"


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

    assert len(results) == 1
    assert results[0]["url"] == "page1"


def test_find_query_handles_extra_spaces():
    index = sample_index()

    results = find_query(index, "   good   friends   ")

    assert len(results) == 1
    assert results[0]["url"] == "page1"


def test_find_query_repeated_terms_do_not_inflate_score():
    index = sample_index()

    normal_results = find_query(index, "good")
    repeated_results = find_query(index, "good good")

    assert repeated_results == normal_results
    
def test_suggest_terms_returns_close_matches_for_misspelled_word():
    index = sample_index()

    suggestions = suggest_terms(index, "frends")

    assert "friends" in suggestions


def test_suggest_terms_ignores_words_already_in_index():
    index = sample_index()

    suggestions = suggest_terms(index, "good frends")

    assert "good" not in suggestions
    assert "friends" in suggestions


def test_suggest_terms_returns_empty_list_for_valid_query():
    index = sample_index()

    suggestions = suggest_terms(index, "good friends")

    assert suggestions == []


def test_suggest_terms_returns_empty_list_for_empty_query():
    index = sample_index()

    suggestions = suggest_terms(index, "")

    assert suggestions == []