from fastapi import APIRouter

from app.core.reporter import generate_report
from app.core.orchestrator import orchestrate
from app.models.schemas import AuditRequest, AuditResponse
from app.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/audit", response_model=AuditResponse)
async def run_audit(request: AuditRequest) -> AuditResponse:
    logger.info(f"Audit requested for URL: {request.url}")

    seed_url = str(request.url)

    result = await orchestrate(seed_url)

    logger.info(
        f"Crawled {result.pages_crawled} pages in {result.crawl_duration_seconds:.2f}s"
    )
    logger.info(f"Audit complete — site score: {result.site_score}")

    return generate_report(result)
