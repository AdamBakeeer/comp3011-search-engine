from src.indexer import tokenize


def print_word(index, word):
    tokens = tokenize(word)

    if not tokens:
        return None

    return index.get(tokens[0])


def find_query(index, query):
    query_words = tokenize(query)

    if not query_words:
        return []

    page_sets = []

    for word in query_words:
        if word not in index:
            return []

        page_sets.append(set(index[word].keys()))

    matching_pages = set.intersection(*page_sets)

    results = []
    for url in matching_pages:
        score = sum(index[word][url]["frequency"] for word in query_words)
        results.append({
            "url": url,
            "score": score
        })

    return sorted(results, key=lambda result: result["score"], reverse=True)