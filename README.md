# COMP3011 Search Engine Coursework

Tests

A lightweight search engine implemented in Python for the COMP3011 coursework assignment. The project crawls the website https://quotes.toscrape.com/, builds an inverted index with positional statistics, persists the index to disk, and provides a command-line interface for searching indexed pages.

---

# Features

- Focused web crawler with pagination traversal
- Configurable politeness window
- Inverted index with:
  - word frequencies
  - positional indexing
- Persistent JSON-based index storage
- Command-line search interface
- Single-word and multi-word search
- Boolean AND retrieval
- TF-IDF ranking
- Query suggestions for misspelled words
- Comprehensive automated test suite
- Coverage analysis with pytest-cov
- Continuous Integration using GitHub Actions
- Benchmarking and complexity analysis

---

# Requirements

- Python 3.12+
- pip

---

# Quick Start

Clone the repository:

bash git clone https://github.com/AdamBakeeer/comp3011-search-engine.git cd comp3011-search-engine 

Install dependencies:

bash pip install -r requirements.txt 

Run the application:

bash python -m src.main 

---

# Project Structure

text comp3011-search-engine/ │ ├── src/ │   ├── crawler.py │   ├── indexer.py │   ├── search.py │   └── main.py │ ├── tests/ │   ├── test_crawler.py │   ├── test_indexer.py │   ├── test_search.py │   └── test_main.py │ ├── data/ │   └── index.json │ ├── .github/workflows/ │   └── tests.yml │ ├── benchmark.py ├── requirements.txt ├── pytest.ini └── README.md 

---

# System Architecture

The system is divided into four main components.

## 1. Crawler

The crawler sequentially traverses the paginated quotes website while respecting a configurable politeness window.

### Responsibilities

- Fetch HTML pages
- Extract quote text
- Follow pagination links
- Prevent duplicate crawling
- Handle request failures gracefully

### Key Design Decisions

- Focused crawler rather than a general-purpose crawler
- BeautifulSoup CSS selectors for precise extraction
- Visited-set tracking for duplicate prevention
- Configurable delay for testing and benchmarking

---

## 2. Indexer

The indexer builds an inverted index from crawled pages.

### Structure

text word -> page URL -> statistics 

Each indexed term stores:
- frequency
- token positions

### Example

json "life": {   "https://quotes.toscrape.com/page/2/": {     "frequency": 4,     "positions": [1, 45, 67, 80]   } } 

Positional indexing was included to support future extensibility toward phrase-search retrieval.

### Key Design Decisions

- Inverted indexing for efficient retrieval
- Positional indexing for extensibility
- Regex-based tokenisation
- JSON persistence for simplicity and transparency

---

## 3. Search Engine

The search engine supports:

- Single-word queries
- Multi-word queries
- Boolean AND retrieval
- TF-IDF ranking
- Query suggestions

### Example Query

text find good friends 

Only pages containing all query terms are returned.

### TF-IDF Ranking

The search engine uses TF-IDF weighting:

text TF-IDF = Term Frequency × Inverse Document Frequency 

This reduces the influence of overly common words and improves retrieval quality.

### Query Suggestions

Query suggestions use approximate string matching via Python’s difflib.

Example:

text find frends 

Output:

text Did you mean: friends? 

---

## 4. Command-Line Interface

The CLI integrates crawling, indexing, persistence, and retrieval into a simple interactive shell.

### Supported Commands

text build load print <word> find <query> exit 

---

# Installation

## Clone the Repository

bash git clone https://github.com/AdamBakeeer/comp3011-search-engine.git cd comp3011-search-engine 

## Create Virtual Environment (Optional)

bash python -m venv venv source venv/bin/activate 

## Install Dependencies

bash pip install -r requirements.txt 

---

# Usage

Run the CLI:

bash python -m src.main 

### Example Session

text Search Engine Tool Commands: build, load, print <word>, find <query>, exit  > build Index built and saved. Pages indexed: 10  > load Index loaded successfully.  > print life {...}  > find good friends https://quotes.toscrape.com/page/2/ | score: 4.355955  > find frends No results found. Did you mean: friends?  > exit Goodbye. 

---

# Testing

Run the automated test suite:

bash pytest 

Run tests with coverage:

bash pytest --cov=src --cov-report=term-missing 

### Test Suite Coverage

The test suite includes:

- Crawler tests
- Indexing tests
- Search tests
- CLI tests
- Edge-case testing
- Exception handling
- Mocked network requests

---

# Test Coverage

Current coverage results:

- crawler.py → 91%
- indexer.py → 100%
- search.py → 100%
- main.py → 72%

Overall project coverage: approximately 87%.

The crawler intentionally does not reach 100% coverage because the real HTTP request layer was mocked during testing. This was a deliberate design decision to avoid network dependency and ensure deterministic automated tests.

---

# Continuous Integration

The project uses GitHub Actions for automated testing.

On every push or pull request:

- Dependencies are installed automatically
- The test suite executes automatically
- Coverage analysis runs automatically

Workflow file:

text .github/workflows/tests.yml 

---

# Benchmarking

Run benchmarking:

bash python benchmark.py 

### Example Benchmark Results

text Pages crawled: 10 Unique terms: 680 Index file size: 169.89 KB Crawl time without delay: 3.3603s Index build time: 0.0033s Index save time: 0.0143s Search time: 0.000184s 

### Key Observations

- Crawling dominates runtime due to networking overhead
- Indexing is highly efficient due to linear token processing
- Search retrieval is effectively instantaneous
- TF-IDF slightly increases query cost while improving ranking quality

---

# Complexity Analysis

## Crawler

text Time Complexity: O(P) 

Where:
- P = number of pages crawled

Each page is visited once.

---

## Indexer

text Time Complexity: O(N) 

Where:
- N = total number of tokens

Each token is processed exactly once.

---

## Search

Query retrieval complexity depends on:

- Posting-list lookup
- Set intersection
- TF-IDF scoring
- Sorting results

The inverted index avoids scanning every document during retrieval.

---

# Testing Strategy

The project uses deterministic automated testing with mocked dependencies.

## Crawler Tests Validate

- Pagination traversal
- Quote extraction
- Duplicate prevention
- Request failures
- Empty pages
- Partial crawl recovery

## Indexer Tests Validate

- Tokenisation
- Positional indexing
- Persistence
- Frequency counting
- Exception handling

## Search Tests Validate

- Boolean retrieval
- TF-IDF ranking
- Query suggestions
- Punctuation handling
- Case insensitivity
- Malformed input

Network requests are mocked to avoid dependency on live website availability.

---

# GenAI Usage and Critical Reflection

Generative AI tools were used as development assistants for:

- Discussing algorithmic design choices
- Debugging implementation issues
- Generating testing ideas
- Reviewing code structure
- Exploring retrieval strategies such as TF-IDF ranking

However, all AI-generated suggestions were manually reviewed, tested, modified, and validated before integration.

## Challenges Encountered

- Some generated solutions introduced unnecessary complexity
- Some code suggestions failed under edge-case testing
- AI occasionally suggested inefficient or incorrect data structures
- Generated tests initially missed important edge cases such as duplicate crawl loops and deterministic request mocking

## Key Learning Outcomes

Using AI reinforced the importance of:

- Understanding algorithms rather than copying implementations
- Validating generated code through testing
- Benchmarking and profiling performance
- Manually reasoning about trade-offs and system behaviour

---

# Future Improvements

Potential future extensions include:

- Phrase search using positional indexing
- Stemming and stop-word removal
- OR query support
- Ranked snippet generation
- Incremental indexing
- Distributed crawling
- Web-based user interface

---

# Author

Adam Bakeer

GitHub:

https://github.com/AdamBakeeer
