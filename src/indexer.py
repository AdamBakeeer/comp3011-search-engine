"""

Indexer module for the COMP3011 search engine coursework.

This module tokenises crawled page text and builds an inverted index

containing frequency and positional statistics for each word. The index

can also be persisted to disk and reloaded from JSON storage.

"""

import json
import re
from pathlib import Path


INDEX_FILE = Path("data/index.json")


def tokenize(text):
    """

    Convert raw text into normalised word tokens.

    Tokenisation is case-insensitive and removes most punctuation while

    preserving apostrophes inside words.

    Args:

        text: Raw text to tokenise.

    Returns:

        A list of lowercase word tokens.

    """
    
    return re.findall(r"\b[a-zA-Z']+\b", text.lower())



def build_index(pages):
    """

    Build an inverted index from crawled pages.

    The inverted index maps:

        word -> page URL -> statistics

    Each indexed word stores:

        - frequency: number of occurrences in the page

        - positions: token positions within the page

    Args:

        pages: A list of crawled pages containing URL and text data.

    Returns:

        A nested dictionary representing the inverted index.

    """
    
    index = {}

    for page in pages:
        url = page["url"]
        tokens = tokenize(page["text"])

        for position, word in enumerate(tokens):
            if word not in index:
                index[word] = {}

            if url not in index[word]:
                index[word][url] = {
                    "frequency": 0,
                    "positions": []
                }

            index[word][url]["frequency"] += 1
            index[word][url]["positions"].append(position)

    return index

def save_index(index, file_path=INDEX_FILE):
    """

    Save the inverted index to a JSON file.

    Args:

        index: The inverted index to persist.

        file_path: Destination path for the saved index.

    """
    
    file_path.parent.mkdir(exist_ok=True)
    
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(index, file, indent=2)

def load_index(file_path=INDEX_FILE):
    """

    Load a previously saved inverted index from disk.

    Args:

        file_path: Path to the saved index file.

    Returns:

        The loaded inverted index.

    Raises:

        FileNotFoundError: If the index file does not exist.

    """
    
    if not file_path.exists():
        raise FileNotFoundError(f"Index file not found: {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)