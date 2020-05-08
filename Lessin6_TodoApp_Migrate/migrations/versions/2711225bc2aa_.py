"""empty message

Revision ID: 2711225bc2aa
Revises: d4b50a4fd39d
Create Date: 2020-05-02 07:55:55.212904

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2711225bc2aa'
down_revision = 'd4b50a4fd39d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('todos')
    # ### end Alembic commands ###