"""empty message

Revision ID: 2873eab246cd
Revises: 6f1a43bb1221
Create Date: 2020-05-02 16:44:32.601480

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2873eab246cd'
down_revision = '6f1a43bb1221'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todolists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('todos', sa.Column('todolist_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'todos', 'todolists', ['todolist_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'todos', type_='foreignkey')
    op.drop_column('todos', 'todolist_id')
    op.drop_table('todolists')
    # ### end Alembic commands ###