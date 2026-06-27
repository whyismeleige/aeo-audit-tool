import enum
import uuid

from sqlalchemy import (
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


class BrandProjectStatus(enum.Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"


brand_projects_table = Table(
    "brand_projects",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "organization_id",
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="RESTRICT"),
        nullable=False,
    ),
    Column(
        "created_by_user_id",
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    ),
    Column("name", Text, nullable=False),
    Column("brand_name", Text, nullable=False),
    Column("canonical_domain", Text, nullable=False),
    Column("market", Text, nullable=True),
    Column("language_code", Text, nullable=True),
    Column("country_code", Text, nullable=True),
    Column("category", Text, nullable=True),
    Column("description", Text, nullable=True),
    Column(
        "status",
        Enum(
            BrandProjectStatus,
            name="brand_project_status",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
        default=BrandProjectStatus.ACTIVE,
        server_default=BrandProjectStatus.ACTIVE.value,
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
    Column("deleted_at", DateTime(timezone=True), nullable=True),
    Index("ix_brand_projects_organization_id", "organization_id"),
    Index("ix_brand_projects_created_by_user_id", "created_by_user_id"),
    Index("ix_brand_projects_brand_name", "brand_name"),
    Index("ix_brand_projects_canonical_domain", "canonical_domain"),
    Index("ix_brand_projects_status", "status"),
    Index("ix_brand_projects_org_name", "organization_id", "name"),
)
