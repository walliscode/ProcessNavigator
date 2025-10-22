# instance/development_config.py
# Copy this file to instance/development_config.py and modify as needed

import os

# Secret key for session management
# IMPORTANT: Change this to a random string in production!
# You can generate a secure key with: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY = 'dev-secret-key-change-this-in-production'

# Database configuration
# Format: postgresql://username:password@host:port/database
# For PostgreSQL (recommended):
SQLALCHEMY_DATABASE_URI = 'postgresql://processnavigator:test@localhost:5432/processnavigator'

# Alternative database URIs for other systems:
# For SQLite (development/testing only):
# SQLALCHEMY_DATABASE_URI = 'sqlite:///processnavigator.db'
# For MySQL:
# SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost:3306/processnavigator'

# Disable SQLAlchemy track modifications to save resources
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Enable debug mode for development
DEBUG = True
