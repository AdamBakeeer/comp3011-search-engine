import time
from pathlib import Path

from src.crawler import crawl_site
from src.indexer import build_index, save_index
from src.search import find_query


def main():
    print("Benchmark Results")
    print("-----------------")

    crawl_start = time.perf_counter()
    pages = crawl_site(delay=0)
    crawl_time = time.perf_counter() - crawl_start

    index_start = time.perf_counter()
    index = build_index(pages)
    index_time = time.perf_counter() - index_start

    save_start = time.perf_counter()
    save_index(index)
    save_time = time.perf_counter() - save_start

    search_start = time.perf_counter()
    results = find_query(index, "good friends")
    search_time = time.perf_counter() - search_start

    index_file = Path("data/index.json")
    index_size_kb = index_file.stat().st_size / 1024

    print(f"Pages crawled: {len(pages)}")
    print(f"Unique terms: {len(index)}")
    print(f"Index file size: {index_size_kb:.2f} KB")
    print(f"Crawl time without delay: {crawl_time:.4f}s")
    print(f"Index build time: {index_time:.4f}s")
    print(f"Index save time: {save_time:.4f}s")
    print(f"Search time: {search_time:.6f}s")
    print(f"Search results returned: {len(results)}")


if __name__ == "__main__":
    main()