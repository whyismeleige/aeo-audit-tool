from app.models.schemas import (
    AuditResponse,
    CategoryScoreResponse,
    PageResponse,
    UnreachablePageResponse,
)
from app.core.orchestrator import OrchestrationResult
from app.core.scorer import ScoreResult, UnreachablePage, CategoryScore


def _map_category_response(category: CategoryScore) -> CategoryScoreResponse:
    return CategoryScoreResponse(
        score=category.score,
        max_possible=category.max_possible,
        metrics=category.metrics,
        findings=category.findings,
        recommendations=category.recommendations,
    )


def _map_page_response(page: ScoreResult) -> PageResponse:
    return PageResponse(
        url=page.url,
        overall_score=page.overall_score,
        metadata=_map_category_response(page.metadata),
        content_quality=_map_category_response(page.content_quality),
        structured_data=_map_category_response(page.structured_data),
        connectivity=_map_category_response(page.connectivity),
        technical_compliance=_map_category_response(page.technical_compliance),
    )


def _map_unreachable_page_response(page: UnreachablePage) -> UnreachablePageResponse:
    return UnreachablePageResponse(
        url=page.url,
        status_code=page.status_code,
        reason=page.reason,
    )


def generate_report(result: OrchestrationResult) -> AuditResponse:
    return AuditResponse(
        url=result.url,
        pages_crawled=result.pages_crawled,
        overall_score=result.site_score,
        findings=result.findings,
        recommendations=result.recommendations,
        pages=[_map_page_response(page) for page in result.pages],
        unreachable_pages=[
            _map_unreachable_page_response(page) for page in result.unreachable_pages
        ],
        crawl_duration_seconds=result.crawl_duration_seconds,
    )
