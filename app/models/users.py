import enum
import uuid

from sqlalchemy import (
    VARCHAR,
    Table,
    Column,
    UUID,
    String,
    Enum,
    DateTime,
    Index,
)
from sqlalchemy.sql import func

from app.models.base import metadata

class UserStatus(enum.Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    DELETED = "deleted"


users_table = Table(
    "users",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("clerk_user_id", String(255), nullable=False, unique=True),
    Column("email", VARCHAR(255), nullable=False, unique=True),
    Column("full_name", String(255), nullable=True),
    Column("avatar_url", String(2048), nullable=True),
    Column(
        "status",
        Enum(
            UserStatus,
            name="user_status",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        default=UserStatus.ACTIVE,
        server_default=UserStatus.ACTIVE.value,
    ),
    Column("last_seen_at", DateTime(timezone=True), nullable=True),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column(
        "updated_at",
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    ),
    Index("ix_users_clerk_user_id", "clerk_user_id", unique=True),
    Index("ix_users_email", "email", unique=True),
    Index("ix_users_status", "status"),
)
