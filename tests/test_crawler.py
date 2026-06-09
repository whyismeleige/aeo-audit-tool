import pytest
from app.core.crawler import Crawler

@pytest.fixture
def crawler():
    return Crawler(seed_url="https://example.com")

@pytest.mark.parametrize("url, base_url, expected", [
    ("/about", "https://example.com/blog", "https://example.com/about"),
    ("/about#section", "https://example.com/blog", "https://example.com/about"),
    ("/about?q=1234", "https://example.com/blog", "https://example.com/about"),
    ("https://google.com", "https://example.com/blog", None),
    ("ftp://example.com", "https://example.com/blog", None),
    ("/about/", "https://example.com/blog", "https://example.com/about"),
    ("/ABoUt", "https://example.com/blog", "https://example.com/about"),
    ("/page", "https://example.com:8080/other", "https://example.com/page")
])
def test_normalize_url(crawler, url, base_url, expected):
    result = crawler._normalize_url(url, base_url)
    assert result == expected

@pytest.mark.parametrize("html, base_url, expected", [
    ("""
    <html>
        <body>
            <a href="/about">About</a>
            <a href="/blog">Blog</a>
        </body>
    </html>
    """, "https://example.com", ["https://example.com/about", "https://example.com/blog"]),
    ("""
    <html>
        <body>
            <a href="/about">About</a>
            <a href="/blog">Blog</a>
            <a href="https://google.com">Google</a>
        </body>
    </html>
    """, "https://example.com", ["https://example.com/about", "https://example.com/blog"]),
    ("""
    <html>
        <body>
            <a href="/about">About</a>
            <a href="">Blog</a>
        </body>
    </html>
    """, "https://example.com", ["https://example.com/about", "https://example.com"]),
    ("""
    <html>
        <body>
        </body>
    </html>
    """, "https://example.com", []),
])    
def test_extract_links(crawler, html, base_url, expected):
    result = crawler._extract_links(html, base_url)
    assert result == expected