from app.core.orchestrator import OrchestrationResult
from app.core.scorer import ScoreResult, CategoryScore

fake_category = CategoryScore(
    score=80,
    max_possible=100,
    metrics={"test": 80},
    findings=["Good"],
    recommendations=[],
)

fake_page = ScoreResult(
    url="https://example.com",
    overall_score=80,
    metadata=fake_category,
    content_quality=fake_category,
    structured_data=fake_category,
    connectivity=fake_category,
    technical_compliance=fake_category,
)

fake_result = OrchestrationResult(
    url="https://example.com",
    site_score=80,
    pages=[fake_page],
    unreachable_pages=[],
    pages_crawled=1,
    crawl_duration_seconds=1.5,
    findings=["Good content"],
    recommendations=["Add schema"],
)