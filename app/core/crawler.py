import asyncio
from collections import deque
from dataclasses import dataclass
from urllib.parse import urlparse

from app.logger import get_logger
from app.config import get_settings

settings = get_settings()
logger = get_logger(__name__) 

@dataclass
class CrawlResult:
    url: str
    html: str
    status_code: int
    
class Crawler:
    def __init__(self, seed_url: str, limit: int = None):
        self.seed_url = seed_url
        self.limit = limit if limit is not None else settings.CRAWL_LIMIT
        
        self.visited: set[str] = set()
        self.queue: deque[str] = deque()
        self.results: list[CrawlResult] = []
        
        self.domain = urlparse(seed_url).netloc
        
        self._semaphore = asyncio.Semaphore(3)
        
        
        
        