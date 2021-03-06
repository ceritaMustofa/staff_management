"""Delete table staff

Revision ID: 25ccabe73770
Revises: 4757b98a26ed
Create Date: 2022-02-21 03:59:38.220906

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '25ccabe73770'
down_revision = '4757b98a26ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('staff')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('staff',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('fullname', mysql.VARCHAR(length=200), nullable=True),
    sa.Column('birth_place', mysql.VARCHAR(length=200), nullable=True),
    sa.Column('birthday', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('staff_identity', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('position_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['position_id'], ['position.id'], name='staff_ibfk_1'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='staff_ibfk_2', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
