import enum
import uuid

from sqlalchemy import Table, Column, UUID, Enum, DateTime, ForeignKey, Text, Index
from sqlalchemy.sql import func

from app.models.base import metadata

class CompetitorStatus(enum.Enum):
    ACTIVE = "active"
    IGNORED = "ignored"
    ARCHIVED = "archived"

competitors_table = Table(
    "competitors",
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
        ForeignKey("brand_projects.id", ondelete="RESTRICT"),
        nullable=False,
    ),
    Column("name", Text, nullable=False),
    Column("canonical_domain", Text, nullable=True),
    Column("category", Text, nullable=True),
    Column("market", Text, nullable=True),
    Column("notes", Text, nullable=True),
    Column(
        "status",
        Enum(
            CompetitorStatus,
            name="competitor_status",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
        default=CompetitorStatus.ACTIVE,
        server_default=CompetitorStatus.ACTIVE.value,
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
    Index("ix_competitors_organization_id", "organization_id"),
    Index("ix_competitors_project_id", "project_id"),
    Index("ix_competitors_name", "name"),
    Index("ix_competitors_canonical_domain", "canonical_domain"),
    Index("ix_competitors_status", "status"),
    Index("ix_competitors_project_name", "project_id", "name"),
)
