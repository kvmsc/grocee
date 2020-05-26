"""Added all tables

Revision ID: d7533d81abd4
Revises: 
Create Date: 2020-05-26 23:12:47.990945

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7533d81abd4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('brand',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('imgurl', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('imgurl', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shop',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=30), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('imgurl', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_shop_email'), 'shop', ['email'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.Column('email', sa.String(length=30), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('brand_category',
    sa.Column('brand_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['brand_id'], ['brand.id'], ),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('brand_id', 'category_id')
    )
    op.create_table('commodity',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('cat_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cat_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('cat_id', sa.Integer(), nullable=False),
    sa.Column('com_id', sa.Integer(), nullable=False),
    sa.Column('brand_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['brand_id'], ['brand.id'], ),
    sa.ForeignKeyConstraint(['cat_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['com_id'], ['commodity.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('variant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('prod_id', sa.Integer(), nullable=False),
    sa.Column('qty', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['prod_id'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shop_variant',
    sa.Column('shop_id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('prod_id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['variant.id'], ),
    sa.ForeignKeyConstraint(['prod_id'], ['product.id'], ),
    sa.ForeignKeyConstraint(['shop_id'], ['shop.id'], ),
    sa.PrimaryKeyConstraint('shop_id', 'item_id')
    )
    op.create_index(op.f('ix_shop_variant_prod_id'), 'shop_variant', ['prod_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_shop_variant_prod_id'), table_name='shop_variant')
    op.drop_table('shop_variant')
    op.drop_table('variant')
    op.drop_table('product')
    op.drop_table('commodity')
    op.drop_table('brand_category')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_shop_email'), table_name='shop')
    op.drop_table('shop')
    op.drop_table('category')
    op.drop_table('brand')
    # ### end Alembic commands ###
