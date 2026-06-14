from fastapi import APIRouter, HTTPException

from app.core.reporter import generate_report
from app.core.orchestrator import orchestrate
from app.models.schemas import AuditRequest, AuditResponse
from app.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/audit", response_model=AuditResponse)
async def run_audit(request: AuditRequest) -> AuditResponse:
    logger.info(f"Audit requested for URL: {request.url}")

    try:
        seed_url = str(request.url)
        result = await orchestrate(seed_url)

        if result.pages_crawled == 0:
            raise HTTPException(
                status_code=503,
                detail="The target website could not be reached. Please verify the URL and try again.",
            )

        if not result.pages:
            raise HTTPException(
                status_code=403,
                detail="All pages on the domain were blocked from crawling. Check robots.txt restrictions.",
            )

        logger.info(
            f"Crawled {result.pages_crawled} pages in {result.crawl_duration_seconds:.2f}s"
        )
        logger.info(f"Audit complete — site score: {result.site_score}")

        return generate_report(result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during audit: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occured during the audit. Please try again.",
        )
