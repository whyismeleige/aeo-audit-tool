"""create_visibility_enums

Revision ID: 1069b2073a81
Revises: e3f2ece0a4b1
Create Date: 2026-06-27 02:28:27.236337

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "1069b2073a81"
down_revision: Union[str, Sequence[str], None] = "e3f2ece0a4b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    sa.Enum("active", "disabled", "deleted", name="user_status").create(op.get_bind())
    sa.Enum("free", "pro", "agency", "enterprise", name="organization_plan").create(op.get_bind())
    sa.Enum("active", "suspended", "cancelled", name="organization_status").create(op.get_bind())
    sa.Enum("owner", "admin", "member", "viewer", name="membership_role").create(op.get_bind())
    sa.Enum("active", "invited", "removed", name="membership_status").create(op.get_bind())
    sa.Enum("active", "paused", "archived", name="brand_project_status").create(op.get_bind())

def downgrade() -> None:
    """Downgrade schema."""
    sa.Enum(name="brand_project_status").drop(op.get_bind())
    sa.Enum(name="membership_status").drop(op.get_bind())
    sa.Enum(name="membership_role").drop(op.get_bind())
    sa.Enum(name="organization_status").drop(op.get_bind())
    sa.Enum(name="organization_plan").drop(op.get_bind())
    sa.Enum(name="user_status").drop(op.get_bind())
