import pytest
from app.core.utils import normalize_url

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
def test_normalize_url(url, base_url, expected):
    result = normalize_url(url, base_url)
    assert result == expected