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
    Table,
    Text,
    UUID,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.models.base import metadata


class PromptRunStatus(enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    TIMEOUT = "timeout"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


prompt_runs_table = Table(
    "prompt_runs",
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
        "prompt_set_id",
        UUID(as_uuid=True),
        ForeignKey("prompt_sets.id", ondelete="RESTRICT"),
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
        "run_number",
        Integer,
        nullable=False,
        default=1,
        server_default=sa.text("1"),
    ),
    Column(
        "status",
        Enum(
            PromptRunStatus,
            name="prompt_run_status",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
        default=PromptRunStatus.PENDING,
        server_default=PromptRunStatus.PENDING.value,
    ),
    Column("prompt_text_snapshot", Text, nullable=False),
    Column("prompt_hash_snapshot", Text, nullable=False),
    Column("provider_name", Text, nullable=True),
    Column("model_name", Text, nullable=True),
    Column("locale", Text, nullable=True),
    Column("region", Text, nullable=True),
    Column("device_type", Text, nullable=True),
    Column("started_at", DateTime(timezone=True), nullable=True),
    Column("completed_at", DateTime(timezone=True), nullable=True),
    Column("latency_ms", Integer, nullable=True),
    Column(
        "retry_count",
        Integer,
        nullable=False,
        default=0,
        server_default=sa.text("0"),
    ),
    Column("error_code", Text, nullable=True),
    Column("error_message", Text, nullable=True),
    Column(
        "raw_metadata",
        JSONB,
        nullable=False,
        default=dict,
        server_default=sa.text("'{}'::jsonb"),
    ),
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
    Index("ix_prompt_runs_organization_id", "organization_id"),
    Index("ix_prompt_runs_project_id", "project_id"),
    Index("ix_prompt_runs_run_batch_id", "run_batch_id"),
    Index("ix_prompt_runs_prompt_set_id", "prompt_set_id"),
    Index("ix_prompt_runs_prompt_id", "prompt_id"),
    Index("ix_prompt_runs_platform_id", "platform_id"),
    Index("ix_prompt_runs_status", "status"),
    Index("ix_prompt_runs_run_number", "run_number"),
    Index("ix_prompt_runs_completed_at", "completed_at"),
    Index(
        "ix_prompt_runs_batch_prompt_run_number",
        "run_batch_id",
        "prompt_id",
        "run_number",
        unique=True,
    ),
)
