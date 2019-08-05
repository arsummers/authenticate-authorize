"""empty message

Revision ID: 66fa03b26fa8
Revises: 41cbcf5378bf
Create Date: 2019-08-04 21:49:12.708128

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66fa03b26fa8'
down_revision = '41cbcf5378bf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('author',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_name', sa.String(length=256), nullable=True),
    sa.Column('books', sa.String(length=256), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('token', sa.String(length=32), nullable=True),
    sa.Column('token_expiration', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('author_name'),
    sa.UniqueConstraint('books')
    )
    op.create_index(op.f('ix_author_token'), 'author', ['token'], unique=True)
    op.create_index(op.f('ix_author_username'), 'author', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_author_username'), table_name='author')
    op.drop_index(op.f('ix_author_token'), table_name='author')
    op.drop_table('author')
    # ### end Alembic commands ###
