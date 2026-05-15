import requests

from src.crawler import parse_quotes_page, crawl_site


def test_parse_quotes_page_extracts_quotes_and_next_url():
    html = """
    <html>
      <div class="quote">
        <span class="text">“First quote.”</span>
      </div>
      <div class="quote">
        <span class="text">“Second quote.”</span>
      </div>
      <li class="next">
        <a href="/page/2/">Next</a>
      </li>
    </html>
    """

    result = parse_quotes_page(html, "https://quotes.toscrape.com/")

    assert result["url"] == "https://quotes.toscrape.com/"
    assert result["text"] == "“First quote.” “Second quote.”"
    assert result["next_url"] == "https://quotes.toscrape.com/page/2/"


def test_parse_quotes_page_returns_none_when_no_next_page():
    html = """
    <html>
      <div class="quote">
        <span class="text">“Final quote.”</span>
      </div>
    </html>
    """

    result = parse_quotes_page(html, "https://quotes.toscrape.com/page/10/")

    assert result["text"] == "“Final quote.”"
    assert result["next_url"] is None


def test_parse_quotes_page_handles_page_with_no_quotes():
    html = """
    <html>
      <p>No quotes here.</p>
    </html>
    """

    result = parse_quotes_page(html, "https://quotes.toscrape.com/empty/")

    assert result["url"] == "https://quotes.toscrape.com/empty/"
    assert result["text"] == ""
    assert result["next_url"] is None


def test_crawl_site_uses_fetch_page_and_follows_pagination(monkeypatch):
    pages = {
        "https://quotes.toscrape.com/": """
            <div class="quote"><span class="text">“Page one quote.”</span></div>
            <li class="next"><a href="/page/2/">Next</a></li>
        """,
        "https://quotes.toscrape.com/page/2/": """
            <div class="quote"><span class="text">“Page two quote.”</span></div>
        """,
    }

    def fake_fetch_page(url):
        return pages[url]

    monkeypatch.setattr("src.crawler.fetch_page", fake_fetch_page)

    result = crawl_site(delay=0)

    assert len(result) == 2
    assert result[0]["url"] == "https://quotes.toscrape.com/"
    assert result[0]["text"] == "“Page one quote.”"
    assert result[1]["url"] == "https://quotes.toscrape.com/page/2/"
    assert result[1]["text"] == "“Page two quote.”"


def test_crawl_site_stops_gracefully_on_request_error(monkeypatch):
    def fake_fetch_page(url):
        raise requests.RequestException("Network failure")

    monkeypatch.setattr("src.crawler.fetch_page", fake_fetch_page)

    result = crawl_site(delay=0)

    assert result == []