import enum
import uuid

import sqlalchemy as sa
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Index,
    Table,
    Text,
    UUID,
)
from sqlalchemy.sql import func

from app.models.base import metadata


class AIProviderType(enum.Enum):
    UI_SCRAPE = "ui_scrape"
    API = "api"
    THIRD_PARTY_API = "third_party_api"
    MANUAL_IMPORT = "manual_import"


ai_platforms_table = Table(
    "ai_platforms",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("code", Text, nullable=False),
    Column("name", Text, nullable=False),
    Column(
        "provider_type",
        Enum(
            AIProviderType,
            name="ai_provider_type",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
    ),
    Column(
        "supports_citations",
        Boolean,
        nullable=False,
        default=False,
        server_default=sa.text("false"),
    ),
    Column(
        "supports_search_queries",
        Boolean,
        nullable=False,
        default=False,
        server_default=sa.text("false"),
    ),
    Column(
        "supports_shopping_cards",
        Boolean,
        nullable=False,
        default=False,
        server_default=sa.text("false"),
    ),
    Column(
        "is_active",
        Boolean,
        nullable=False,
        default=True,
        server_default=sa.text("true"),
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
    Index("ix_ai_platforms_code", "code", unique=True),
    Index("ix_ai_platforms_is_active", "is_active"),
    Index("ix_ai_platforms_provider_type", "provider_type"),
)
