"""empty message

Revision ID: 0c9148482639
Revises: ce9e77a9b081
Create Date: 2024-07-24 06:08:24.943525

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c9148482639'
down_revision = 'ce9e77a9b081'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('fk_users_invite_code', type_='foreignkey')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_foreign_key('fk_users_invite_code', 'invite_code', ['invite_code_code'], ['code'])

    # ### end Alembic commands ###
