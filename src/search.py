"""

Search module for the COMP3011 search engine coursework.

This module provides inverted-index retrieval functionality for

single-word and multi-word queries. Results are ranked using TF-IDF

(term frequency–inverse document frequency) scoring.

"""

from src.indexer import tokenize
import math
import difflib

def print_word(index, word):
    """

    Retrieve the inverted index entry for a single word.

    The lookup is case-insensitive because tokenisation normalises

    all text to lowercase.

    Args:

        index: The inverted index.

        word: The word to retrieve.

    Returns:

        The posting list for the word if present, otherwise None.

    """
    
    tokens = tokenize(word)

    if not tokens:
        return None

    return index.get(tokens[0])

def get_total_documents(index):
    """

    Count the total number of unique documents in the index.

    Args:

        index: The inverted index.

    Returns:

        The number of unique indexed documents.

    """
    
    documents = set()

    for posting_list in index.values():
        documents.update(posting_list.keys())

    return len(documents)


def calculate_tfidf_score(index, word, url, total_documents):
    """

    Calculate the TF-IDF score for a word within a document.

    TF-IDF increases the importance of words that occur frequently

    within a document while reducing the influence of overly common

    words across the full document collection.

    Args:

        index: The inverted index.

        word: The query word being scored.

        url: The document URL.

        total_documents: Total number of indexed documents.

    Returns:

        The TF-IDF score for the word in the document.

    """
    term_frequency = index[word][url]["frequency"]
    document_frequency = len(index[word])

    inverse_document_frequency = math.log(
        (total_documents + 1) / (document_frequency + 1)
    ) + 1

    return term_frequency * inverse_document_frequency


def find_query(index, query):
    """

    Find documents matching a multi-word query.

    The search engine uses Boolean AND retrieval, meaning only

    documents containing all query terms are returned.

    Matching documents are ranked using summed TF-IDF scores.

    Args:

        index: The inverted index.

        query: User search query.

    Returns:

        A ranked list of matching documents and scores.

    """
    query_words = tokenize(query)

    if not query_words:
        return []

    query_words = list(dict.fromkeys(query_words))
    
    page_sets = []

    for word in query_words:
        if word not in index:
            return []

        page_sets.append(set(index[word].keys()))

    matching_pages = set.intersection(*page_sets)
    total_documents = get_total_documents(index)

    results = []
    for url in matching_pages:
        score = sum(calculate_tfidf_score(index, word, url, total_documents)
            for word in query_words)
        results.append({
            "url": url,
            "score": round(score, 6)
        })

    return sorted(results, key=lambda result: result["score"], reverse=True)

def suggest_terms(index: dict, query: str, limit: int = 3) -> list[str]:
    """
    Suggest similar indexed terms for words not found in the index.

    Args:
        index: The inverted index.
        query: User search query.
        limit: Maximum number of suggestions per missing word.

    Returns:
        A list of suggested indexed terms.
    """
    query_words = tokenize(query)

    if not query_words:
        return []

    suggestions = []

    for word in query_words:
        if word in index:
            continue

        matches = difflib.get_close_matches(
            word,
            index.keys(),
            n=limit,
            cutoff=0.8,
        )

        suggestions.extend(matches)

    return list(dict.fromkeys(suggestions))