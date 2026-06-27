import uuid

import sqlalchemy as sa
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    Table,
    UUID,
)
from sqlalchemy.sql import func

from app.models.base import metadata


prompt_set_prompts_table = Table(
    "prompt_set_prompts",
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
        ForeignKey("prompt_sets.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "prompt_id",
        UUID(as_uuid=True),
        ForeignKey("prompts.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("position", Integer, nullable=False, default=0, server_default=sa.text("0")),
    Column("weight", Numeric, nullable=False, default=1, server_default=sa.text("1")),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
    Index("ix_prompt_set_prompts_organization_id", "organization_id"),
    Index("ix_prompt_set_prompts_project_id", "project_id"),
    Index("ix_prompt_set_prompts_prompt_set_id", "prompt_set_id"),
    Index("ix_prompt_set_prompts_prompt_id", "prompt_id"),
    Index(
        "ix_prompt_set_prompts_set_prompt",
        "prompt_set_id",
        "prompt_id",
        unique=True,
    ),
)
