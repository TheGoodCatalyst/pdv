"""create user_profiles and credentials tables

Revision ID: 0001
Revises: 
Create Date: 2024-01-01 00:00:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'user_profiles',
        sa.Column('user_id', sa.String(), primary_key=True, index=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), unique=True, index=True),
        sa.Column('dob', sa.DateTime()),
        sa.Column('preferences', sa.JSON())
    )
    op.create_table(
        'credentials',
        sa.Column('user_id', sa.String(), primary_key=True),
        sa.Column('cred_type', sa.String(), primary_key=True),
        sa.Column('issued_at', sa.DateTime(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('status', sa.Enum('active', 'revoked', 'expired', name='credentialstatus'), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('blob', sa.LargeBinary(), nullable=False)
    )

def downgrade():
    op.drop_table('credentials')
    op.drop_table('user_profiles')
