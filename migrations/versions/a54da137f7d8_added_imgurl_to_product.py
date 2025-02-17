"""added imgurl to product

Revision ID: a54da137f7d8
Revises: d7533d81abd4
Create Date: 2020-05-26 23:50:42.181845

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a54da137f7d8'
down_revision = 'd7533d81abd4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('imgurl', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'imgurl')
    # ### end Alembic commands ###
