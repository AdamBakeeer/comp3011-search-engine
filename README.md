COMP3011 Search Engine Coursework

A lightweight search engine implemented in Python for the COMP3011 coursework assignment. The project crawls the website https://quotes.toscrape.com/, builds an inverted index with positional statistics, persists the index to disk, and provides a command-line interface for searching indexed pages.

⸻

Features

* Focused web crawler with pagination traversal
* Configurable politeness window
* Inverted index with:
    * word frequencies
    * positional indexing
* Persistent JSON-based index storage
* Command-line search interface
* Single-word and multi-word search
* Boolean AND retrieval
* TF-IDF ranking
* Query suggestions for misspelled words
* Comprehensive automated test suite
* Coverage analysis with pytest-cov
* Continuous Integration using GitHub Actions
* Benchmarking and complexity analysis

⸻

Project Structure

comp3011-search-engine/
│
├── src/
│   ├── crawler.py
│   ├── indexer.py
│   ├── search.py
│   └── main.py
│
├── tests/
│   ├── test_crawler.py
│   ├── test_indexer.py
│   ├── test_search.py
│   └── test_main.py
│
├── data/
│   └── index.json
│
├── benchmark.py
├── requirements.txt
├── pytest.ini
└── README.md

⸻

System Architecture

The system is divided into four main components:

1. Crawler

The crawler sequentially traverses the paginated quotes website while respecting a configurable politeness window.

Responsibilities:

* fetch HTML pages
* extract quote text
* follow pagination links
* prevent duplicate crawling
* handle request failures gracefully

Key design decisions:

* focused crawler rather than general-purpose crawler
* BeautifulSoup CSS selectors for precise extraction
* visited-set tracking for duplicate prevention
* configurable delay for testing and benchmarking

⸻

2. Indexer

The indexer builds an inverted index from crawled pages.

Structure:

word -> page URL -> statistics

Each indexed term stores:

* frequency
* token positions

Example:

"life": {
  "https://quotes.toscrape.com/page/2/": {
    "frequency": 4,
    "positions": [1, 45, 67, 80]
  }
}

Key design decisions:

* inverted indexing for efficient retrieval
* positional indexing for future extensibility
* regex-based tokenisation
* JSON persistence for simplicity and transparency

⸻

3. Search Engine

The search engine supports:

* single-word queries
* multi-word queries
* Boolean AND retrieval
* TF-IDF ranking
* query suggestions

Example:

find good friends

Only pages containing all query terms are returned.

Ranking uses TF-IDF weighting:

TF-IDF = Term Frequency × Inverse Document Frequency

This reduces the influence of overly common words and improves retrieval quality.

Query suggestions use lightweight string similarity matching via Python’s difflib.

Example:

find frends

Output:

Did you mean: friends?

⸻

4. Command-Line Interface

The CLI integrates crawling, indexing, persistence, and retrieval into a simple interactive shell.

Supported commands:

build
load
print <word>
find <query>
exit

⸻

Installation

Clone the repository

git clone https://github.com/AdamBakeeer/comp3011-search-engine.git
cd comp3011-search-engine

Create virtual environment (optional)

python -m venv venv
source venv/bin/activate

Install dependencies

pip install -r requirements.txt


⸻

Usage

Run the CLI:

python -m src.main

Example session:

Search Engine Tool
Commands: build, load, print <word>, find <query>, exit
> build
Index built and saved. Pages indexed: 10
> load
Index loaded successfully.
> print life
{...}
> find good friends
https://quotes.toscrape.com/page/2/ | score: 4.355955
> find frends
No results found.
Did you mean: friends?
> exit
Goodbye.

⸻

Testing

Run the automated test suite:

pytest

Run tests with coverage:

pytest --cov=src --cov-report=term-missing

The test suite includes:

* crawler tests
* indexing tests
* search tests
* CLI tests
* edge-case testing
* exception handling
* mocked network requests

⸻

Continuous Integration

The project uses GitHub Actions for automated testing.

On every push or pull request:

* dependencies are installed
* the test suite executes automatically
* coverage analysis runs automatically

Workflow file:

.github/workflows/tests.yml

⸻

Benchmarking

Run benchmarking:

python benchmark.py

Example benchmark results:

Pages crawled: 10
Unique terms: 680
Index file size: 169.89 KB
Crawl time without delay: 3.3603s
Index build time: 0.0033s
Index save time: 0.0143s
Search time: 0.000184s

Key observations:

* crawling dominates runtime due to networking overhead
* indexing is highly efficient due to linear token processing
* search retrieval is effectively instantaneous
* TF-IDF slightly increases query cost while improving ranking quality

⸻

Complexity Analysis

Crawler

Time Complexity: O(P)

Where:

* P = number of pages crawled

Each page is visited once.

⸻

Indexer

Time Complexity: O(N)

Where:

* N = total number of tokens

Each token is processed exactly once.

⸻

Search

Query retrieval complexity depends on:

* posting-list lookup
* set intersection
* TF-IDF scoring
* sorting results

The inverted index avoids scanning every document during retrieval.

⸻

Testing Strategy

The project uses deterministic automated testing with mocked dependencies.

Crawler tests validate:

* pagination traversal
* quote extraction
* duplicate prevention
* request failures
* empty pages
* partial crawl recovery

Indexer tests validate:

* tokenisation
* positional indexing
* persistence
* frequency counting
* exception handling

Search tests validate:

* Boolean retrieval
* TF-IDF ranking
* query suggestions
* punctuation handling
* case insensitivity
* malformed input

Network requests are mocked to avoid dependency on live website availability.

⸻

GenAI Usage and Critical Reflection

Generative AI tools were used as development assistants for:

* discussing algorithmic design choices
* debugging implementation issues
* generating testing ideas
* reviewing code structure
* exploring retrieval strategies such as TF-IDF ranking

However, all AI-generated suggestions were manually reviewed, tested, modified, and validated before integration.

Challenges encountered when using AI:

* some generated solutions introduced unnecessary complexity
* some code suggestions failed under edge-case testing
* AI occasionally suggested inefficient or incorrect data structures
* generated tests initially missed important edge cases such as duplicate crawl loops and deterministic request mocking

Using AI reinforced the importance of:

* understanding algorithms rather than copying implementations
* validating generated code through testing
* benchmarking and profiling performance
* manually reasoning about trade-offs and system behaviour

⸻

Future Improvements

Potential future extensions include:

* phrase search using positional indexing
* stemming and stop-word removal
* OR query support
* ranked snippet generation
* incremental indexing
* distributed crawling
* web-based user interface

⸻

Author

Adam Bakeer

GitHub:

https://github.com/AdamBakeeer
