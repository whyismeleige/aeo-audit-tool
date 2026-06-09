from dataclasses import dataclass, field

from bs4 import BeautifulSoup

from app.logger import get_logger
from app.config import get_settings

settings = get_settings()
logger = get_logger(__name__)


@dataclass
class FAQItem:
    question: str
    answer: str


@dataclass
class ParsedPage:
    url: str
    status_code: int
    word_count: int
    has_schema: bool
    images_without_alt: int
    title: str | None = None
    meta_description: str | None = None
    meta_robots: str | None = None
    canonical_url: str | None = None
    body_text_content: str | None = None
    headings: list[str] = field(default_factory=list)
    internal_links: list[str] = field(default_factory=list)
    json_ld_schema: list[str] = field(default_factory=list)
    schema_types: list[str] = field(default_factory=list)
    faq_items: list[FAQItem] = field(default_factory=list)

def _extract_title(soup: BeautifulSoup) -> str | None:
    return soup.title.string if soup.title else None

def _extract_meta_description(soup: BeautifulSoup) -> str | None:
    meta = soup.find("meta", attrs={"name": "description"})
    return meta.get("content") if meta else None

def _extract_meta_robots(soup: BeautifulSoup) -> str | None:
    meta = soup.find("meta", attrs={"name": "robots"})
    return meta.get("content") if meta else None