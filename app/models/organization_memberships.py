import enum
import uuid

from sqlalchemy import (
    Table,
    Column,
    UUID,
    Enum,
    DateTime,
    ForeignKey,
    Index,
)
from sqlalchemy.sql import func

from app.models.base import metadata


class MembershipRole(enum.Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"


class MembershipStatus(enum.Enum):
    ACTIVE = "active"
    INVITED = "invited"
    REMOVED = "removed"


organization_memberships_table = Table(
    "organization_memberships",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "organization_id",
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "role",
        Enum(
            MembershipRole,
            name="membership_role",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
        default=MembershipRole.MEMBER,
        server_default=MembershipRole.MEMBER.value,
    ),
    Column(
        "status",
        Enum(
            MembershipStatus,
            name="membership_status",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
        default=MembershipStatus.ACTIVE,
        server_default=MembershipStatus.ACTIVE.value,
    ),
    Column(
        "invited_by_user_id",
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    ),
    Column("joined_at", DateTime(timezone=True), nullable=True),
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
    Index(
        "ix_organization_memberships_org_user",
        "organization_id",
        "user_id",
        unique=True,
    ),
    Index("ix_organization_memberships_organization_id", "organization_id"),
    Index("ix_organization_memberships_user_id", "user_id"),
    Index("ix_organization_memberships_role", "role"),
    Index("ix_organization_memberships_status", "status"),
)
