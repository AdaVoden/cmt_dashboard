"""split

Revision ID: 7fc51d825069
Revises: 47fc847fce7d
Create Date: 2022-01-14 15:18:27.875870

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fc51d825069'
down_revision = '47fc847fce7d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sqm',
    sa.Column('time', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('brightness', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('time', name=op.f('pk_sqm')),
    sa.UniqueConstraint('time', name=op.f('uq_sqm_time'))
    )
    op.drop_column('weather', 'brightness')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('weather', sa.Column('brightness', sa.FLOAT(), nullable=True))
    op.drop_table('sqm')
    # ### end Alembic commands ###
