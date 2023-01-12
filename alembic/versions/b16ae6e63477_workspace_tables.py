"""workspace tables

Revision ID: b16ae6e63477
Revises: bef4a0594c74
Create Date: 2023-01-12 21:12:30.807469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b16ae6e63477"
down_revision = "bef4a0594c74"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "workspace",
        sa.Column("id", sa.Integer),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("is_premium", sa.Boolean(), nullable=False),
        sa.Column("revoke_link", sa.Boolean(), server_default=sa.text("false")),
        sa.Column(
            "date_created", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")
        ),
        sa.Column(
            "date_updated", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], ondelete="SET NULL"),
    )

    op.create_table(
        "workspace_member",
        sa.Column("id", sa.Integer),
        sa.Column("workspace_id", sa.Integer(), nullable=False),
        sa.Column("member_id", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column(
            "date_created", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")
        ),
        sa.Column(
            "date_updated", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspace.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["member_id"], ["users.id"], ondelete="CASCADE"),
    )
    pass


def downgrade() -> None:
    op.drop_constraint("workspace_created_by_fkey", table_name="workspace")
    op.drop_constraint("workspace_member_member_id_fkey", table_name="workspace_member")
    op.drop_constraint(
        "workspace_member_workspace_id_fkey", table_name="workspace_member"
    )
    op.drop_table("workspace")
    op.drop_table("workspace_member")
    pass
