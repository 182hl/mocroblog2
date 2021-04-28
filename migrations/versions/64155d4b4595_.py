"""empty message

Revision ID: 64155d4b4595
Revises: 07198f78c30d
Create Date: 2021-04-25 22:32:51.614037

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64155d4b4595'
down_revision = '07198f78c30d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('language', sa.String(length=5), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'language')
    # ### end Alembic commands ###
