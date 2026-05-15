from src.indexer import tokenize
import math


def print_word(index, word):
    tokens = tokenize(word)

    if not tokens:
        return None

    return index.get(tokens[0])

def get_total_documents(index):
    documents = set()

    for posting_list in index.values():
        documents.update(posting_list.keys())

    return len(documents)


def calculate_tfidf_score(index, word, url, total_documents):
    term_frequency = index[word][url]["frequency"]
    document_frequency = len(index[word])

    inverse_document_frequency = math.log(
        (total_documents + 1) / (document_frequency + 1)
    ) + 1

    return term_frequency * inverse_document_frequency


def find_query(index, query):
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