"""implement relationships

Revision ID: c1a7258c056a
Revises: b44dcfc8bacb
Create Date: 2024-04-25 14:32:24.740057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1a7258c056a'
down_revision = 'b44dcfc8bacb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('signups', schema=None) as batch_op:
        batch_op.add_column(sa.Column('camper_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('activity_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_signups_activity_id_activities'), 'activities', ['activity_id'], ['id'])
        batch_op.create_foreign_key(batch_op.f('fk_signups_camper_id_campers'), 'campers', ['camper_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('signups', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_signups_camper_id_campers'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('fk_signups_activity_id_activities'), type_='foreignkey')
        batch_op.drop_column('activity_id')
        batch_op.drop_column('camper_id')

    # ### end Alembic commands ###
