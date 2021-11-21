"""Added users, races, words and statistics

Revision ID: 142a27c463a4
Revises: 
Create Date: 2021-11-20 11:48:33.623352

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '142a27c463a4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('race',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('ranking', sa.Integer(), nullable=False),
    sa.Column('total_participants', sa.Integer(), nullable=True),
    sa.Column('wpm', sa.Integer(), nullable=True),
    sa.Column('epm', sa.Integer(), nullable=True),
    sa.Column('accuracy', sa.Integer(), nullable=True),
    sa.Column('time', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('statistics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('best_wpm', sa.Integer(), nullable=True),
    sa.Column('total_races', sa.Integer(), nullable=True),
    sa.Column('total_wins', sa.Integer(), nullable=True),
    sa.Column('average_wpm', sa.Integer(), nullable=True),
    sa.Column('average_epm', sa.Integer(), nullable=True),
    sa.Column('average_accurasy', sa.Integer(), nullable=True),
    sa.Column('average_time', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=False),
    sa.Column('password_hash', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('words',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('words', sa.String(length=1000), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('words')
    op.drop_table('user')
    op.drop_table('statistics')
    op.drop_table('race')
    # ### end Alembic commands ###