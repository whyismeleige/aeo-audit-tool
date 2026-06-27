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
from sqlalchemy.sql import func

from app.models.base import metadata


class DomainType(enum.Enum):
    MAIN = "main"
    BLOG = "blog"
    DOCS = "docs"
    STORE = "store"
    SUPPORT = "support"
    SOCIAL = "social"
    MARKETPLACE = "marketplace"
    OTHER = "other"


competitor_domains_table = Table(
    "competitor_domains",
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
        "competitor_id",
        UUID(as_uuid=True),
        ForeignKey("competitors.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("domain", Text, nullable=False),
    Column(
        "domain_type",
        Enum(
            DomainType,
            name="domain_type",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
        default=DomainType.MAIN,
        server_default=DomainType.MAIN.value,
    ),
    Column(
        "is_primary",
        Boolean,
        nullable=False,
        default=False,
        server_default=sa.text("false"),
    ),
    Column(
        "created_at", DateTime(timezone=True), server_default=func.now(), nullable=False
    ),
    Column(
        "updated_at",
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    ),
    Index("ix_competitor_domains_organization_id", "organization_id"),
    Index("ix_competitor_domains_project_id", "project_id"),
    Index("ix_competitor_domains_competitor_id", "competitor_id"),
    Index("ix_competitor_domains_domain", "domain"),
    Index(
        "ix_competitor_domains_competitor_domain",
        "competitor_id",
        "domain",
        unique=True,
    ),
)
