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


class RunBatchType(enum.Enum):
    MANUAL = "manual"
    SCHEDULED = "scheduled"
    BACKFILL = "backfill"
    TEST = "test"


class RunBatchStatus(enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PARTIAL = "partial"


run_batches_table = Table(
    "run_batches",
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
        ForeignKey("prompt_sets.id", ondelete="RESTRICT"),
        nullable=False,
    ),
    Column(
        "platform_id",
        UUID(as_uuid=True),
        ForeignKey("ai_platforms.id", ondelete="RESTRICT"),
        nullable=False,
    ),
    Column(
        "created_by_user_id",
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    ),
    Column("name", Text, nullable=False),
    Column(
        "run_type",
        Enum(
            RunBatchType,
            name="run_batch_type",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
        default=RunBatchType.MANUAL,
        server_default=RunBatchType.MANUAL.value,
    ),
    Column(
        "status",
        Enum(
            RunBatchStatus,
            name="run_batch_status",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
        default=RunBatchStatus.PENDING,
        server_default=RunBatchStatus.PENDING.value,
    ),
    Column(
        "repeats_per_prompt",
        Integer,
        nullable=False,
        default=1,
        server_default=sa.text("1"),
    ),
    Column("scheduled_at", DateTime(timezone=True), nullable=True),
    Column("started_at", DateTime(timezone=True), nullable=True),
    Column("completed_at", DateTime(timezone=True), nullable=True),
    Column(
        "config",
        JSONB,
        nullable=False,
        default=dict,
        server_default=sa.text("'{}'::jsonb"),
    ),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column(
        "updated_at",
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    ),
    Column(
        "deleted_at",
        DateTime(timezone=True),
        nullable=True
    ),
    Index("ix_run_batches_organization_id", "organization_id"),
    Index("ix_run_batches_project_id", "project_id"),
    Index("ix_run_batches_prompt_set_id", "prompt_set_id"),
    Index("ix_run_batches_platform_id", "platform_id"),
    Index("ix_run_batches_created_by_user_id", "created_by_user_id"),
    Index("ix_run_batches_status", "status"),
    Index("ix_run_batches_scheduled_at", "scheduled_at"),
    Index("ix_run_batches_started_at", "started_at"),
    Index("ix_run_batches_completed_at", "completed_at"),
)
