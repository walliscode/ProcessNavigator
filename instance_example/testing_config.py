# instance/testing_config.py
# Copy this file to instance/testing_config.py for running tests

import os

# Secret key for testing
SECRET_KEY = 'test-secret-key'

# Use in-memory SQLite for fast testing
# This creates a temporary database that's destroyed after tests complete
SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Alternative: Use a persistent test database (slower but more realistic)
# SQLALCHEMY_DATABASE_URI = 'postgresql://processnavigator:test@localhost:5432/processnavigator_test'

# Disable SQLAlchemy track modifications
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Disable CSRF for testing (allows form submission without CSRF tokens)
WTF_CSRF_ENABLED = False

# Testing mode
TESTING = True
