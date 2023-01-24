"""Added about and admin fields

Revision ID: ad6586c67557
Revises: 9e5525ae862c
Create Date: 2023-01-24 12:45:20.487330

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad6586c67557'
down_revision = '9e5525ae862c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('about_author', sa.Text(length=500), nullable=True))
    op.add_column('users', sa.Column('admin', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'admin')
    op.drop_column('users', 'about_author')
    # ### end Alembic commands ###
