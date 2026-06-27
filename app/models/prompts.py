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
    Table,
    Text,
    UUID,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.models.base import metadata


class PromptIntentType(enum.Enum):
    BEST_PRODUCT = "best_product"
    COMPARISON = "comparison"
    REVIEW = "review"
    RECOMMENDATION = "recommendation"
    PROBLEM_SOLUTION = "problem_solution"
    BRAND_CHECK = "brand_check"
    INFORMATIONAL = "informational"
    TRANSACTIONAL = "transactional"
    LOCAL_SEARCH = "local_search"


class PromptBuyerStage(enum.Enum):
    AWARENESS = "awareness"
    CONSIDERATION = "consideration"
    PURCHASE = "purchase"
    POST_PURCHASE = "post_purchase"


prompts_table = Table(
    "prompts",
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
        "created_by_user_id",
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    ),
    Column("prompt_text", Text, nullable=False),
    Column("prompt_hash", Text, nullable=False),
    Column("language_code", Text, nullable=True),
    Column("country_code", Text, nullable=True),
    Column("category", Text, nullable=True),
    Column(
        "intent_type",
        Enum(
            PromptIntentType,
            name="prompt_intent_type",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
    ),
    Column(
        "buyer_stage",
        Enum(
            PromptBuyerStage,
            name="prompt_buyer_stage",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=True,
    ),
    Column("persona", Text, nullable=True),
    Column("expected_brand", Text, nullable=True),
    Column(
        "is_active",
        Boolean,
        nullable=False,
        default=True,
        server_default=sa.text("true"),
    ),
    Column(
        "prompt_metadata",
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
    Column("deleted_at", DateTime(timezone=True), nullable=True),
    Index("ix_prompts_organization_id", "organization_id"),
    Index("ix_prompts_project_id", "project_id"),
    Index("ix_prompts_created_by_user_id", "created_by_user_id"),
    Index("ix_prompts_prompt_hash", "prompt_hash"),
    Index("ix_prompts_intent_type", "intent_type"),
    Index("ix_prompts_buyer_stage", "buyer_stage"),
    Index("ix_prompts_is_active", "is_active"),
    Index("ix_prompts_project_prompt_hash", "project_id", "prompt_hash", unique=True),
)
