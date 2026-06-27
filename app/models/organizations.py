import enum
import uuid

from sqlalchemy import (
    Table,
    Column,
    UUID,
    String,
    Enum,
    DateTime,
    ForeignKey,
    Index,
)
from sqlalchemy.sql import func

from app.models.base import metadata


class OrganizationPlan(enum.Enum):
    FREE = "free"
    PRO = "pro"
    AGENCY = "agency"
    ENTERPRISE = "enterprise"


class OrganizationStatus(enum.Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"


organizations_table = Table(
    "organizations",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("clerk_org_id", String(255), nullable=True),
    Column("name", String(255), nullable=False),
    Column("slug", String(255), nullable=False),
    Column(
        "owner_user_id",
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    ),
    Column(
        "plan",
        Enum(
            OrganizationPlan,
            name="organization_plan",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
        default=OrganizationPlan.FREE,
        server_default=OrganizationPlan.FREE.value,
    ),
    Column(
        "status",
        Enum(
            OrganizationStatus,
            name="organization_status",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
        default=OrganizationStatus.ACTIVE,
        server_default=OrganizationStatus.ACTIVE.value,
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
    Index("ix_organizations_clerk_org_id", "clerk_org_id", unique=True),
    Index("ix_organizations_slug", "slug", unique=True),
    Index("ix_organizations_owner_user_id", "owner_user_id"),
    Index("ix_organizations_status", "status"),
)
