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
    Table,
    Text,
    UUID,
)
from sqlalchemy.sql import func

from app.models.base import metadata


class CitationGapType(enum.Enum):
    BRAND_MENTIONED_NOT_CITED = "brand_mentioned_not_cited"
    COMPETITOR_CITED_BRAND_NOT_CITED = "competitor_cited_brand_not_cited"
    THIRD_PARTY_DOMINATES = "third_party_dominates"
    OWNED_CONTENT_MISSING = "owned_content_missing"
    WEAK_OWNED_PAGE = "weak_owned_page"


class CitationGapSeverity(enum.Enum):
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"
    CRITICAL = "critical"


class CitationGapStatus(enum.Enum):
    OPEN = "open"
    REVIEWED = "reviewed"
    FIXED = "fixed"
    IGNORED = "ignored"
    ARCHIVED = "archived"


citation_gaps_table = Table(
    "citation_gaps",
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
        "prompt_id",
        UUID(as_uuid=True),
        ForeignKey("prompts.id", ondelete="SET NULL"),
        nullable=True,
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
        "competitor_id",
        UUID(as_uuid=True),
        ForeignKey("competitors.id", ondelete="SET NULL"),
        nullable=True,
    ),

    Column(
        "evidence_observation_id",
        UUID(as_uuid=True),
        ForeignKey("ai_observations.id", ondelete="SET NULL"),
        nullable=True,
    ),
    Column(
        "evidence_citation_id",
        UUID(as_uuid=True),
        ForeignKey("citations.id", ondelete="SET NULL"),
        nullable=True,
    ),

    Column(
        "gap_type",
        Enum(
            CitationGapType,
            name="citation_gap_type",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
    ),
    Column(
        "severity",
        Enum(
            CitationGapSeverity,
            name="citation_gap_severity",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
        default=CitationGapSeverity.MEDIUM,
        server_default=CitationGapSeverity.MEDIUM.value,
    ),

    Column("source_domain", Text, nullable=True),
    Column("source_url", Text, nullable=True),

    Column(
        "evidence_count",
        Integer,
        nullable=False,
        default=1,
        server_default=sa.text("1"),
    ),

    Column(
        "owned_domain_present",
        Boolean,
        nullable=False,
        default=False,
        server_default=sa.text("false"),
    ),
    Column(
        "competitor_present",
        Boolean,
        nullable=False,
        default=False,
        server_default=sa.text("false"),
    ),
    Column(
        "brand_mentioned",
        Boolean,
        nullable=False,
        default=False,
        server_default=sa.text("false"),
    ),
    Column(
        "brand_recommended",
        Boolean,
        nullable=False,
        default=False,
        server_default=sa.text("false"),
    ),

    Column("recommended_action", Text, nullable=True),

    Column(
        "status",
        Enum(
            CitationGapStatus,
            name="citation_gap_status",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
        default=CitationGapStatus.OPEN,
        server_default=CitationGapStatus.OPEN.value,
    ),

    Column("first_seen_at", DateTime(timezone=True), nullable=False),
    Column("last_seen_at", DateTime(timezone=True), nullable=False),

    Column(
        "created_at",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    ),
    Column(
        "updated_at",
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    ),

    Index("ix_citation_gaps_organization_id", "organization_id"),
    Index("ix_citation_gaps_project_id", "project_id"),
    Index("ix_citation_gaps_prompt_id", "prompt_id"),
    Index("ix_citation_gaps_prompt_set_id", "prompt_set_id"),
    Index("ix_citation_gaps_run_batch_id", "run_batch_id"),
    Index("ix_citation_gaps_platform_id", "platform_id"),
    Index("ix_citation_gaps_competitor_id", "competitor_id"),
    Index("ix_citation_gaps_evidence_observation_id", "evidence_observation_id"),
    Index("ix_citation_gaps_evidence_citation_id", "evidence_citation_id"),
    Index("ix_citation_gaps_gap_type", "gap_type"),
    Index("ix_citation_gaps_severity", "severity"),
    Index("ix_citation_gaps_status", "status"),
    Index("ix_citation_gaps_source_domain", "source_domain"),
    Index("ix_citation_gaps_first_seen_at", "first_seen_at"),
    Index("ix_citation_gaps_last_seen_at", "last_seen_at"),
)
