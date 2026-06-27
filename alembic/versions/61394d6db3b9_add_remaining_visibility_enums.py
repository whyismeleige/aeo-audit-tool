"""add_remaining_visibility_enums

Revision ID: 61394d6db3b9
Revises: f852f7358045
Create Date: 2026-06-27 17:44:07.926453

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "61394d6db3b9"
down_revision: Union[str, Sequence[str], None] = "f852f7358045"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

ENUMS = {
    "domain_type": [
        "main",
        "blog",
        "docs",
        "store",
        "support",
        "social",
        "marketplace",
        "other",
    ],
    "competitor_status": [
        "active",
        "ignored",
        "archived",
    ],
    "prompt_set_status": [
        "draft",
        "active",
        "archived",
    ],
    "prompt_intent_type": [
        "best_product",
        "comparison",
        "review",
        "recommendation",
        "problem_solution",
        "brand_check",
        "informational",
        "transactional",
        "local_search",
    ],
    "prompt_buyer_stage": [
        "awareness",
        "consideration",
        "purchase",
        "post_purchase",
    ],
    "ai_provider_type": [
        "ui_scrape",
        "api",
        "third_party_api",
        "manual_import",
    ],
    "run_batch_type": [
        "manual",
        "scheduled",
        "backfill",
        "test",
    ],
    "run_batch_status": [
        "pending",
        "running",
        "completed",
        "failed",
        "cancelled",
        "partial",
    ],
    "prompt_run_status": [
        "pending",
        "running",
        "succeeded",
        "failed",
        "timeout",
        "blocked",
        "cancelled",
    ],
    "extraction_status": [
        "pending",
        "succeeded",
        "failed",
        "partial",
    ],
    "extraction_method": [
        "regex",
        "llm",
        "hybrid",
        "manual",
    ],
    "source_category": [
        "owned",
        "competitor",
        "marketplace",
        "publisher",
        "forum",
        "social",
        "unknown",
    ],
    "mention_type": [
        "neutral",
        "recommendation",
        "comparison",
        "warning",
        "product_listing",
    ],
    "sentiment_type": [
        "positive",
        "neutral",
        "negative",
        "mixed",
        "unknown",
    ],
    "recommendation_strength": [
        "strong",
        "medium",
        "weak",
        "none",
        "unknown",
    ],
    "ranking_entity_type": [
        "brand",
        "competitor",
        "other",
    ],
    "ranking_basis": [
        "explicit_numbered_list",
        "order_of_mention",
        "recommendation_order",
        "inferred",
    ],
    "metric_snapshot_type": [
        "batch",
        "daily",
        "weekly",
        "monthly",
        "manual_report",
    ],
    "citation_gap_type": [
        "brand_mentioned_not_cited",
        "competitor_cited_brand_not_cited",
        "third_party_dominates",
        "owned_content_missing",
        "weak_owned_page",
    ],
    "citation_gap_severity": [
        "low",
        "medium",
        "high",
        "critical",
    ],
    "citation_gap_status": [
        "open",
        "reviewed",
        "fixed",
        "ignored",
        "archived",
    ],
}


def upgrade() -> None:
    bind = op.get_bind()

    for enum_name, enum_values in ENUMS.items():
        sa.Enum(*enum_values, name=enum_name).create(bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()

    for enum_name in reversed(ENUMS.keys()):
        sa.Enum(name=enum_name).drop(bind, checkfirst=True)
