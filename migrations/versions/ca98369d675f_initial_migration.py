"""Initial migration.

Revision ID: ca98369d675f
Revises: 
Create Date: 2021-07-29 19:01:00.188612

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca98369d675f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('author', sa.String(length=50), nullable=False),
    sa.Column('publication_date', sa.DateTime(), nullable=True),
    sa.Column('isbn', sa.BigInteger(), nullable=False),
    sa.Column('number_of_pages', sa.Integer(), nullable=False),
    sa.Column('book_cover_link', sa.String(length=50), nullable=False),
    sa.Column('publication_language', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('isbn')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('books')
    # ### end Alembic commands ###
