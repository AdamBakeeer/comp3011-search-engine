import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://quotes.toscrape.com/"
POLITENESS_DELAY = 6


def fetch_page(url):
    """Fetch a page and return its HTML content."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text


def parse_quotes_page(html, url):
    """Extract quote text from a page and find the next page URL."""
    soup = BeautifulSoup(html, "html.parser")

    quotes = []
    for quote in soup.select(".quote .text"):
        quotes.append(quote.get_text(strip=True))

    next_link = soup.select_one("li.next a")
    next_url = urljoin(url, next_link["href"]) if next_link else None

    return {
        "url": url,
        "text": " ".join(quotes),
        "next_url": next_url,
    }


def crawl_site(start_url=BASE_URL, delay=POLITENESS_DELAY):
    """Crawl all quote pages and return extracted text for each page."""
    pages = []
    visited = set()
    current_url = start_url

    while current_url and current_url not in visited:
        visited.add(current_url)

        try:
            html = fetch_page(current_url)
            page_data = parse_quotes_page(html, current_url)
            pages.append({
                "url": page_data["url"],
                "text": page_data["text"],
            })
            current_url = page_data["next_url"]

            if current_url:
                time.sleep(delay)

        except requests.RequestException as error:
            print(f"Failed to crawl {current_url}: {error}")
            break

    return pages