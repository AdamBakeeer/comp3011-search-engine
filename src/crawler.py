"""

Crawler module for the COMP3011 search engine coursework.

This module implements a focused crawler for https://quotes.toscrape.com/.

It fetches quote pages, extracts quote text, follows pagination links, and

returns structured page data for indexing.

"""

import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://quotes.toscrape.com/"
POLITENESS_DELAY = 6


def fetch_page(url):
    """

    Fetch the HTML content for a single URL.

    Args:

        url: The page URL to request.

    Returns:

        The HTML content of the page as a string.

    Raises:

        requests.RequestException: If the request fails or returns an error status.

    """
    
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text


def parse_quotes_page(html, url):
    """

    Extract quote text and the next-page URL from a quotes page.

    Args:

        html: Raw HTML content returned by the crawler.

        url: The URL of the page being parsed.

    Returns:

        A dictionary containing:

            - url: the current page URL

            - text: all extracted quote text joined into one string

            - next_url: the absolute URL of the next page, or None if absent

    """
    
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
    """

    Crawl the paginated quotes website and extract text from each page.

    The crawler follows only the pagination link to keep crawling focused on

    the target website content. A visited set is used to avoid duplicate URLs

    and prevent accidental loops. The delay parameter enforces the required

    politeness window during normal crawling, while allowing tests to run with

    delay=0.

    Args:

        start_url: URL where crawling should begin.

        delay: Number of seconds to wait between page requests.

    Returns:

        A list of dictionaries, where each dictionary contains:

            - url: the crawled page URL

            - text: extracted quote text from that page

    """
    
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