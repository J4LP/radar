"""empty message

Revision ID: 18c0abd1e31
Revises: None
Create Date: 2015-06-10 17:42:44.248429

"""

# revision identifiers, used by Alembic.
import sqlalchemy_utils

revision = '18c0abd1e31'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('eve_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('solar_system',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('region', sa.String(), nullable=True),
    sa.Column('region_id', sa.Integer(), nullable=True),
    sa.Column('constellation', sa.String(), nullable=True),
    sa.Column('constellation_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.Column('main_character', sa.String(), nullable=True),
    sa.Column('main_character_id', sa.Integer(), nullable=True),
    sa.Column('alliance_name', sa.String(), nullable=True),
    sa.Column('corporation_name', sa.String(), nullable=True),
    sa.Column('last_ip', sqlalchemy_utils.types.ip_address.IPAddressType(length=50), nullable=True),
    sa.Column('last_login_on', sqlalchemy_utils.types.arrow.ArrowType(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('scan',
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('added_by_id', sa.Integer(), nullable=True),
    sa.Column('created_on', sqlalchemy_utils.types.arrow.ArrowType(), nullable=False),
    sa.Column('updated_on', sqlalchemy_utils.types.arrow.ArrowType(), nullable=False),
    sa.ForeignKeyConstraint(['added_by_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('structure',
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
    sa.Column('eve_type_id', sa.Integer(), nullable=True),
    sa.Column('system_id', sa.Integer(), nullable=True),
    sa.Column('planet', sa.String(), nullable=True),
    sa.Column('planet_id', sa.Integer(), nullable=True),
    sa.Column('corporation', sa.String(), nullable=False),
    sa.Column('corporation_id', sa.Integer(), nullable=False),
    sa.Column('alliance', sa.String(), nullable=True),
    sa.Column('alliance_id', sa.Integer(), nullable=True),
    sa.Column('standing', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('scan_id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=True),
    sa.Column('added_by_id', sa.Integer(), nullable=True),
    sa.Column('created_on', sqlalchemy_utils.types.arrow.ArrowType(), nullable=False),
    sa.Column('updated_on', sqlalchemy_utils.types.arrow.ArrowType(), nullable=False),
    sa.ForeignKeyConstraint(['added_by_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['eve_type_id'], ['eve_type.id'], ),
    sa.ForeignKeyConstraint(['scan_id'], ['scan.id'], ),
    sa.ForeignKeyConstraint(['system_id'], ['solar_system.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('structure')
    op.drop_table('scan')
    op.drop_table('user')
    op.drop_table('solar_system')
    op.drop_table('eve_type')
    ### end Alembic commands ###
