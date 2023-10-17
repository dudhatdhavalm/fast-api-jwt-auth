"""change data type

Revision ID: 6b13384ab9db
Revises: 4c1918129ea7
Create Date: 2023-08-19 15:27:39.531382

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b13384ab9db'
down_revision = '4c1918129ea7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'english_proficiency',
               existing_type=sa.VARCHAR(length=32),
               type_=sa.Integer(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'english_proficiency',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=32),
               existing_nullable=False)
    # ### end Alembic commands ###