# ProcessNavigator Quick Start Guide

This is a quick reference for setting up and running ProcessNavigator.

## 🚀 Quick Setup (5 Minutes)

### 1. Prerequisites Check
```bash
python3 --version  # Should be 3.8+
psql --version     # PostgreSQL should be installed
git --version      # Git should be installed
```

### 2. Clone and Setup
```bash
# Clone the repository
git clone https://github.com/walliscode/ProcessNavigator.git
cd ProcessNavigator

# Create virtual environment
python3 -m venv .venv  # or 'python -m venv .venv' on Windows

# Activate virtual environment
source .venv/bin/activate              # Linux/macOS
# OR
.venv\Scripts\activate                 # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Setup

#### Create PostgreSQL Database
```bash
# Connect to PostgreSQL
psql -U postgres  # Windows/Linux with postgres user
# OR
sudo -u postgres psql  # Linux alternative

# In psql shell, run:
CREATE DATABASE processnavigator;
CREATE USER processnavigator WITH PASSWORD 'test';
ALTER DATABASE processnavigator OWNER TO processnavigator;
GRANT ALL PRIVILEGES ON DATABASE processnavigator TO processnavigator;
\q
```

### 4. Configure Application
```bash
# Create instance directory
mkdir instance

# Copy configuration files
cp instance_example/development_config.py instance/  # Linux/macOS
cp instance_example/testing_config.py instance/
# OR
copy instance_example\development_config.py instance\  # Windows
copy instance_example\testing_config.py instance\

# (Optional) Edit instance/development_config.py to change database credentials
```

### 5. Initialize Database Tables
```bash
# Start Flask shell
flask --app process_navigator shell

# In Python shell:
>>> from process_navigator.extensions.database import db
>>> db.create_all()
>>> exit()
```

### 6. Run the Application
```bash
flask --app process_navigator run --debug
```

Open your browser to: http://127.0.0.1:5000/

## 📋 Common Commands

### Virtual Environment
```bash
# Activate
source .venv/bin/activate              # Linux/macOS
.venv\Scripts\activate                 # Windows

# Deactivate
deactivate
```

### Running the App
```bash
# Development mode (with auto-reload and debug)
flask --app process_navigator run --debug

# Production mode (not recommended for development)
flask --app process_navigator run

# Custom port
flask --app process_navigator run --port 5001 --debug
```

### Database Management
```bash
# Open Flask shell with app context
flask --app process_navigator shell

# In the shell:
>>> from process_navigator.extensions.database import db
>>> db.create_all()        # Create all tables
>>> db.drop_all()          # ⚠️ WARNING: Deletes all data!

# Refresh database (drops and recreates)
flask --app process_navigator refresh-database  # ⚠️ Deletes all data!
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=process_navigator --cov-report=html --cov-report=term

# Run specific test file
pytest tests/test_home_routes.py

# Verbose output
pytest -v
```

### Code Formatting
```bash
# Check formatting (doesn't modify files)
black --check process_navigator/ tests/

# Format code
black process_navigator/ tests/
```

## 🔧 Troubleshooting Quick Fixes

### "Cannot connect to database"
```bash
# Check if PostgreSQL is running
# Windows: Check Services app
# Linux: sudo systemctl status postgresql
# macOS: brew services list

# Verify database exists
psql -U postgres -l

# Test connection
psql -U processnavigator -d processnavigator
```

### "No module named 'process_navigator'"
```bash
# Make sure you're in the project root directory
pwd

# Ensure virtual environment is activated
which python  # Should point to .venv/bin/python

# Reinstall dependencies
pip install -r requirements.txt
```

### "Port 5000 already in use"
```bash
# Use different port
flask --app process_navigator run --port 5001 --debug

# Find process using port 5000
# Linux/macOS: lsof -i :5000
# Windows: netstat -ano | findstr :5000
```

### "Database tables don't exist"
```bash
# Create tables
flask --app process_navigator shell
>>> from process_navigator.extensions.database import db
>>> db.create_all()
>>> exit()
```

## 📚 File Structure Overview

```
ProcessNavigator/
├── instance/                      # Your local config (not in git)
│   ├── development_config.py     # Dev database settings
│   ├── testing_config.py         # Test settings
│   └── file_storage/             # Uploaded files
├── instance_example/              # Config templates
│   ├── development_config.py     # Template to copy
│   ├── testing_config.py         # Template to copy
│   └── README.md                 # Config documentation
├── process_navigator/             # Main application code
│   ├── __init__.py               # App factory
│   ├── models/                   # Database models
│   ├── home/                     # Authentication
│   ├── data/                     # Data management
│   ├── cauldron/                 # Process paths
│   ├── templates/                # HTML templates
│   └── static/                   # CSS, JS, images
├── tests/                         # Test suite
├── .venv/                         # Virtual environment
├── README.md                      # Full documentation
├── requirements.txt               # Python dependencies
└── .gitignore                     # Git ignore rules
```

## 🎯 Next Steps After Setup

1. Register a user account at http://127.0.0.1:5000/register
2. Log in with your credentials
3. Explore the data management features
4. Create process methods, inputs, and parameters
5. Use the Cauldron to create process paths

## 💡 Tips

- Always activate your virtual environment before working on the project
- Use `pytest` before committing code changes
- Use `black` to format your code before committing
- Check `.github/workflows/CI_CD_README.md` for CI/CD documentation
- Read `COPILOT_INSTRUCTIONS.md` for detailed architecture information

## 📖 Full Documentation

For complete documentation, see:
- `README.md` - Comprehensive setup and usage guide
- `PROJECT_PLAN.md` - Project roadmap and features
- `TESTING_FRAMEWORK.md` - Testing documentation
- `COPILOT_INSTRUCTIONS.md` - Architecture and coding standards

## 🆘 Getting Help

If you encounter issues:
1. Check the Troubleshooting section above
2. Review the full `README.md` documentation
3. Check existing GitHub issues
4. Create a new issue with details about your problem

---

**Happy Coding! 🚀**
