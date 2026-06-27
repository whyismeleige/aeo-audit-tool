import enum
import uuid

import sqlalchemy as sa
from sqlalchemy import (
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
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.models.base import metadata


class MetricSnapshotType(enum.Enum):
    BATCH = "batch"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    MANUAL_REPORT = "manual_report"


metric_snapshots_table = Table(
    "metric_snapshots",
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
        "prompt_set_id",
        UUID(as_uuid=True),
        ForeignKey("prompt_sets.id", ondelete="SET NULL"),
        nullable=True,
    ),
    Column(
        "run_batch_id",
        UUID(as_uuid=True),
        ForeignKey("run_batches.id", ondelete="SET NULL"),
        nullable=True,
    ),
    Column(
        "platform_id",
        UUID(as_uuid=True),
        ForeignKey("ai_platforms.id", ondelete="SET NULL"),
        nullable=True,
    ),

    Column(
        "snapshot_type",
        Enum(
            MetricSnapshotType,
            name="metric_snapshot_type",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
    ),

    Column("window_start", DateTime(timezone=True), nullable=False),
    Column("window_end", DateTime(timezone=True), nullable=False),

    Column("total_prompt_runs", Integer, nullable=False, default=0, server_default=sa.text("0")),
    Column("successful_prompt_runs", Integer, nullable=False, default=0, server_default=sa.text("0")),
    Column("failed_prompt_runs", Integer, nullable=False, default=0, server_default=sa.text("0")),
    Column("total_observations", Integer, nullable=False, default=0, server_default=sa.text("0")),

    Column("brand_mention_count", Integer, nullable=False, default=0, server_default=sa.text("0")),
    Column("brand_mention_rate", Numeric, nullable=False, default=0, server_default=sa.text("0")),

    Column("brand_citation_count", Integer, nullable=False, default=0, server_default=sa.text("0")),
    Column("brand_citation_rate", Numeric, nullable=False, default=0, server_default=sa.text("0")),

    Column("brand_recommendation_count", Integer, nullable=False, default=0, server_default=sa.text("0")),
    Column("brand_recommendation_rate", Numeric, nullable=False, default=0, server_default=sa.text("0")),

    Column("avg_brand_rank", Numeric, nullable=True),
    Column("median_brand_rank", Numeric, nullable=True),

    Column("competitor_mention_count", Integer, nullable=False, default=0, server_default=sa.text("0")),
    Column("competitor_recommendation_count", Integer, nullable=False, default=0, server_default=sa.text("0")),

    Column("owned_citation_count", Integer, nullable=False, default=0, server_default=sa.text("0")),
    Column("competitor_citation_count", Integer, nullable=False, default=0, server_default=sa.text("0")),
    Column("third_party_citation_count", Integer, nullable=False, default=0, server_default=sa.text("0")),

    Column("visibility_score", Numeric, nullable=False, default=0, server_default=sa.text("0")),
    Column("citation_score", Numeric, nullable=False, default=0, server_default=sa.text("0")),
    Column("recommendation_score", Numeric, nullable=False, default=0, server_default=sa.text("0")),
    Column("ranking_score", Numeric, nullable=False, default=0, server_default=sa.text("0")),
    Column("sentiment_score", Numeric, nullable=True),
    Column("volatility_score", Numeric, nullable=True),

    Column("methodology_version", Text, nullable=False),

    Column("summary", Text, nullable=True),
    Column(
        "details",
        JSONB,
        nullable=False,
        default=dict,
        server_default=sa.text("'{}'::jsonb"),
    ),

    Column("generated_at", DateTime(timezone=True), nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),

    Index("ix_metric_snapshots_organization_id", "organization_id"),
    Index("ix_metric_snapshots_project_id", "project_id"),
    Index("ix_metric_snapshots_prompt_set_id", "prompt_set_id"),
    Index("ix_metric_snapshots_run_batch_id", "run_batch_id"),
    Index("ix_metric_snapshots_platform_id", "platform_id"),
    Index("ix_metric_snapshots_snapshot_type", "snapshot_type"),
    Index("ix_metric_snapshots_window_start", "window_start"),
    Index("ix_metric_snapshots_window_end", "window_end"),
    Index("ix_metric_snapshots_methodology_version", "methodology_version"),
    Index("ix_metric_snapshots_generated_at", "generated_at"),
)
