"""Initial schema

Revision ID: 001_initial
Revises: 
Create Date: 2025-12-24 17:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('username', sa.String(length=100), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=True),
        sa.Column('full_name', sa.String(length=255), nullable=True),
        sa.Column('role', sa.Enum('ADMIN', 'VOICE_ACTOR', 'CLIENT', 'GUEST', name='userrole'), nullable=False),
        sa.Column('oauth_provider', sa.String(length=50), nullable=True),
        sa.Column('oauth_id', sa.String(length=255), nullable=True),
        sa.Column('avatar_url', sa.String(length=500), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=False),
        sa.Column('two_factor_enabled', sa.Boolean(), nullable=False),
        sa.Column('two_factor_secret', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    
    # Voice actors table
    op.create_table(
        'voice_actors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('stage_name', sa.String(length=255), nullable=True),
        sa.Column('portfolio_url', sa.String(length=500), nullable=True),
        sa.Column('demo_reel_url', sa.String(length=500), nullable=True),
        sa.Column('languages', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('accents', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('specialties', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('total_voices_created', sa.Integer(), nullable=False),
        sa.Column('total_revenue', sa.Float(), nullable=False),
        sa.Column('total_usage_minutes', sa.Float(), nullable=False),
        sa.Column('revenue_share_percentage', sa.Float(), nullable=False),
        sa.Column('auto_approve_licenses', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    
    # Voice models table
    op.create_table(
        'voice_models',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('actor_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('voice_id', sa.String(length=255), nullable=False),
        sa.Column('training_status', sa.Enum('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED', name='trainingstatus'), nullable=False),
        sa.Column('training_started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('training_completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('training_error', sa.Text(), nullable=True),
        sa.Column('sample_audio_url', sa.String(length=500), nullable=True),
        sa.Column('demo_audio_url', sa.String(length=500), nullable=True),
        sa.Column('language', sa.String(length=10), nullable=False),
        sa.Column('accent', sa.String(length=50), nullable=True),
        sa.Column('gender', sa.String(length=20), nullable=True),
        sa.Column('age_range', sa.String(length=20), nullable=True),
        sa.Column('price_per_minute', sa.Float(), nullable=False),
        sa.Column('subscription_price', sa.Float(), nullable=True),
        sa.Column('total_usage_minutes', sa.Float(), nullable=False),
        sa.Column('total_revenue', sa.Float(), nullable=False),
        sa.Column('total_generations', sa.Integer(), nullable=False),
        sa.Column('is_public', sa.Boolean(), nullable=False),
        sa.Column('is_featured', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['actor_id'], ['voice_actors.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_voice_models_voice_id'), 'voice_models', ['voice_id'], unique=True)
    
    # Add more tables as needed...


def downgrade() -> None:
    op.drop_index(op.f('ix_voice_models_voice_id'), table_name='voice_models')
    op.drop_table('voice_models')
    op.drop_table('voice_actors')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.execute('DROP TYPE IF EXISTS userrole')
    op.execute('DROP TYPE IF EXISTS trainingstatus')

