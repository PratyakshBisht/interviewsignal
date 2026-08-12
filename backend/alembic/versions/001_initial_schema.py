"""Initial schema creation

Revision ID: 001_initial
Revises: 
Create Date: 2026-08-12

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('github_id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), nullable=True),
        sa.Column('avatar_url', sa.Text(), nullable=True),
        sa.Column('github_access_token', sa.Text(), nullable=False),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('location', sa.String(255), nullable=True),
        sa.Column('company', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('last_analysis_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_users_github_id', 'users', ['github_id'], unique=True)
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_index('ix_users_email', 'users', ['email'], unique=False)

    # Create analyses table
    op.create_table(
        'analyses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('github_data', sa.JSON(), nullable=True),
        sa.Column('total_repos', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('total_commits', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('code_quality_score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('consistency_score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('depth_score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('production_readiness_score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('overall_score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('recruiter_summary', sa.Text(), nullable=True),
        sa.Column('strengths', sa.JSON(), nullable=True),
        sa.Column('weaknesses', sa.JSON(), nullable=True),
        sa.Column('recommendations', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('analysis_version', sa.String(10), nullable=False, server_default='1.0'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_analyses_id', 'analyses', ['id'], unique=False)
    op.create_index('ix_analyses_user_id', 'analyses', ['user_id'], unique=False)
    op.create_index('idx_user_id_created_at', 'analyses', ['user_id', 'created_at'], unique=False)
    op.create_index('idx_user_id_overall_score', 'analyses', ['user_id', 'overall_score'], unique=False)


def downgrade() -> None:
    op.drop_index('idx_user_id_overall_score', table_name='analyses')
    op.drop_index('idx_user_id_created_at', table_name='analyses')
    op.drop_index('ix_analyses_user_id', table_name='analyses')
    op.drop_index('ix_analyses_id', table_name='analyses')
    op.drop_table('analyses')
    
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_username', table_name='users')
    op.drop_index('ix_users_github_id', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_table('users')
