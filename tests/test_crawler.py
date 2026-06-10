import pytest
from app.core.crawler import Crawler

@pytest.fixture
def crawler():
    return Crawler(seed_url="https://example.com")

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