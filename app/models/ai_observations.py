import uuid

import sqlalchemy as sa
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Table,
    Text,
    UUID,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.models.base import metadata


ai_observations_table = Table(
    "ai_observations",
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

    Column("observed_at", DateTime(timezone=True), nullable=False),

    Column("response_text", Text, nullable=False),
    Column("response_markdown", Text, nullable=True),
    Column("response_html", Text, nullable=True),

    Column("answer_title", Text, nullable=True),
    Column("answer_url", Text, nullable=True),

    Column("model_name", Text, nullable=True),

    Column(
        "citations_raw",
        JSONB,
        nullable=False,
        default=list,
        server_default=sa.text("'[]'::jsonb"),
    ),
    Column(
        "search_queries_raw",
        JSONB,
        nullable=False,
        default=list,
        server_default=sa.text("'[]'::jsonb"),
    ),
    Column(
        "shopping_cards_raw",
        JSONB,
        nullable=False,
        default=list,
        server_default=sa.text("'[]'::jsonb"),
    ),
    Column(
        "followups_raw",
        JSONB,
        nullable=False,
        default=list,
        server_default=sa.text("'[]'::jsonb"),
    ),

    Column(
        "raw_payload",
        JSONB,
        nullable=False,
        default=dict,
        server_default=sa.text("'{}'::jsonb"),
    ),

    Column("screenshot_path", Text, nullable=True),

    Column("content_hash", Text, nullable=False),
    Column(
        "is_empty",
        Boolean,
        nullable=False,
        default=False,
        server_default=sa.text("false"),
    ),

    Column(
        "created_at",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    ),

    Index("ix_ai_observations_organization_id", "organization_id"),
    Index("ix_ai_observations_project_id", "project_id"),
    Index("ix_ai_observations_run_batch_id", "run_batch_id"),
    Index("ix_ai_observations_prompt_run_id", "prompt_run_id"),
    Index("ix_ai_observations_prompt_id", "prompt_id"),
    Index("ix_ai_observations_platform_id", "platform_id"),
    Index("ix_ai_observations_observed_at", "observed_at"),
    Index("ix_ai_observations_content_hash", "content_hash"),
    Index(
        "ix_ai_observations_prompt_run_content_hash",
        "prompt_run_id",
        "content_hash",
        unique=True,
    ),
)
