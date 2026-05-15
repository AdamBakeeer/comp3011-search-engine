import json
import re
from pathlib import Path


INDEX_FILE = Path("data/index.json")


def tokenize(text):
    return re.findall(r"\b[a-zA-Z']+\b", text.lower())



def build_index(pages):
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
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(index, file, indent=2)


def load_index(file_path=INDEX_FILE):
    if not file_path.exists():
        raise FileNotFoundError(f"Index file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)