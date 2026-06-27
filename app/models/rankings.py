import enum
import uuid

import sqlalchemy as sa
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    Table,
    Text,
    UUID,
)
from sqlalchemy.sql import func

from app.models.base import metadata


class RankingEntityType(enum.Enum):
    BRAND = "brand"
    COMPETITOR = "competitor"
    OTHER = "other"


class RankingBasis(enum.Enum):
    EXPLICIT_NUMBERED_LIST = "explicit_numbered_list"
    ORDER_OF_MENTION = "order_of_mention"
    RECOMMENDATION_ORDER = "recommendation_order"
    INFERRED = "inferred"


rankings_table = Table(
    "rankings",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),

    Column(
        "organization_id",
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="RESTRICT"),
        nullable=False,
    ),
    Column(
        "project_id",
        UUID(as_uuid=True),
        ForeignKey("brand_projects.id", ondelete="CASCADE"),
        nullable=False,
    ),

    Column(
        "run_batch_id",
        UUID(as_uuid=True),
        ForeignKey("run_batches.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "prompt_run_id",
        UUID(as_uuid=True),
        ForeignKey("prompt_runs.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "observation_id",
        UUID(as_uuid=True),
        ForeignKey("ai_observations.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "extraction_result_id",
        UUID(as_uuid=True),
        ForeignKey("extraction_results.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "prompt_id",
        UUID(as_uuid=True),
        ForeignKey("prompts.id", ondelete="RESTRICT"),
        nullable=False,
    ),
    Column(
        "platform_id",
        UUID(as_uuid=True),
        ForeignKey("ai_platforms.id", ondelete="RESTRICT"),
        nullable=False,
    ),

    Column(
        "competitor_id",
        UUID(as_uuid=True),
        ForeignKey("competitors.id", ondelete="SET NULL"),
        nullable=True,
    ),

    Column(
        "entity_type",
        Enum(
            RankingEntityType,
            name="ranking_entity_type",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
    ),
    Column("entity_name", Text, nullable=False),

    Column("rank_position", Integer, nullable=False),

    Column(
        "ranking_basis",
        Enum(
            RankingBasis,
            name="ranking_basis",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
    ),
    Column("ranking_context", Text, nullable=True),

    Column(
        "is_recommended",
        Boolean,
        nullable=False,
        default=False,
        server_default=sa.text("false"),
    ),

    Column(
        "confidence_score",
        Numeric,
        nullable=False,
        default=0,
        server_default=sa.text("0"),
    ),

    Column(
        "created_at",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    ),

    Index("ix_rankings_organization_id", "organization_id"),
    Index("ix_rankings_project_id", "project_id"),
    Index("ix_rankings_run_batch_id", "run_batch_id"),
    Index("ix_rankings_prompt_run_id", "prompt_run_id"),
    Index("ix_rankings_observation_id", "observation_id"),
    Index("ix_rankings_extraction_result_id", "extraction_result_id"),
    Index("ix_rankings_prompt_id", "prompt_id"),
    Index("ix_rankings_platform_id", "platform_id"),
    Index("ix_rankings_competitor_id", "competitor_id"),
    Index("ix_rankings_entity_type", "entity_type"),
    Index("ix_rankings_rank_position", "rank_position"),
    Index("ix_rankings_is_recommended", "is_recommended"),
)
