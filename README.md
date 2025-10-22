# ProcessNavigator

![Tests](https://github.com/walliscode/ProcessNavigator/workflows/Tests/badge.svg)
![Code Quality](https://github.com/walliscode/ProcessNavigator/workflows/Code%20Quality/badge.svg)

A Flask-based web application for managing, tracking, and analyzing physical processes with database-driven design-of-experiments capabilities.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Application Configuration](#application-configuration)
- [Running the Application](#running-the-application)
- [Development](#development)
- [CI/CD and Testing](#cicd-and-testing)

## Prerequisites

Before starting, ensure you have the following installed:
- **Python 3.8+** (Python 3.12 recommended)
- **PostgreSQL 12+** (or another DBMS if you modify the configuration)
- **Git** (for cloning the repository)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/walliscode/ProcessNavigator.git
cd ProcessNavigator
```

### 2. Create Virtual Environment

**On Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**On Windows:**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

To update dependencies later:
```bash
pip freeze > requirements.txt
```

## Database Setup

This application is designed to work with PostgreSQL, but can be configured to use other database management systems by modifying the `SQLALCHEMY_DATABASE_URI` in the configuration file.

### PostgreSQL Installation

#### On Windows:
1. Download PostgreSQL from the [official website](https://www.postgresql.org/download/windows/)
2. Run the installer and follow the setup wizard
3. During installation, set a password for the default `postgres` superuser (remember this password!)
4. Note the installation directory (typically `C:\Program Files\PostgreSQL\<version>`)
5. Add PostgreSQL's `bin` folder to your system PATH:
   - Open System Properties → Environment Variables
   - Edit the `Path` variable under System variables
   - Add `C:\Program Files\PostgreSQL\<version>\bin`
   - Click OK to save

#### On Linux (Ubuntu/Debian):
```bash
# Update package lists
sudo apt update

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Check PostgreSQL status
sudo systemctl status postgresql
```

#### On Linux (RHEL/CentOS/Fedora):
```bash
# Install PostgreSQL
sudo dnf install postgresql-server postgresql-contrib

# Initialize the database
sudo postgresql-setup --initdb

# Start and enable PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### On macOS:
```bash
# Using Homebrew
brew install postgresql@15

# Start PostgreSQL service
brew services start postgresql@15
```

### Creating the Database

#### On Windows:
1. Open Command Prompt or PowerShell
2. Connect to PostgreSQL as the superuser:
   ```cmd
   psql -U postgres
   ```
3. Enter the password you set during installation

#### On Linux:
```bash
# Switch to postgres user and open PostgreSQL shell
sudo -u postgres psql
```

#### On macOS:
```bash
# Connect to PostgreSQL
psql postgres
```

#### Database Setup Commands (All Platforms):
Once in the PostgreSQL shell (`psql`), run the following commands:

```sql
-- Create the database
CREATE DATABASE processnavigator;

-- Create a user with password
CREATE USER processnavigator WITH PASSWORD 'test';

-- Grant ownership of the database to the user
ALTER DATABASE processnavigator OWNER TO processnavigator;

-- Grant all privileges (optional, but ensures full access)
GRANT ALL PRIVILEGES ON DATABASE processnavigator TO processnavigator;

-- Exit the PostgreSQL shell
\q
```

**Note:** For production environments, use a strong password instead of 'test'.

### Verify Database Connection

Test your database connection:

**On Windows:**
```cmd
psql -U processnavigator -d processnavigator
```

**On Linux/macOS:**
```bash
psql -U processnavigator -d processnavigator -h localhost
```

You will be prompted for the password ('test' if you followed the setup above). Type `\q` to exit.

## Application Configuration

### 1. Create the Instance Folder

The instance folder stores configuration files and instance-specific data. It's excluded from version control for security.

```bash
mkdir instance
```

### 2. Create Configuration Files

The repository includes example configuration files in the `instance_example/` directory.

**Quick Setup:**

**On Linux/macOS:**
```bash
cp instance_example/development_config.py instance/
cp instance_example/testing_config.py instance/
```

**On Windows:**
```cmd
copy instance_example\development_config.py instance\
copy instance_example\testing_config.py instance\
```

**Edit the Configuration:**

Open `instance/development_config.py` and update if needed:
- Database credentials (username, password, host, port)
- Secret key (generate a secure one: `python -c "import secrets; print(secrets.token_hex(32))"`)

The default configuration assumes:
- Database: `processnavigator`
- User: `processnavigator`
- Password: `test`
- Host: `localhost`
- Port: `5432`

**Important Notes:**
- For **Windows** with PostgreSQL: The default configuration should work as-is
- For **Linux/macOS**: The default configuration should work, but you may need to adjust the host if PostgreSQL uses Unix sockets
- For **production**: Always use strong passwords and secure secret keys. Consider using environment variables for sensitive data
- See `instance_example/README.md` for detailed information about configuration options

### 3. Initialize Database Tables

With your virtual environment activated and configuration files in place:

**On Windows:**
```cmd
flask --app process_navigator shell
```

**On Linux/macOS:**
```bash
flask --app process_navigator shell
```

In the Flask shell, create the database tables:
```python
>>> from process_navigator.extensions.database import db
>>> db.create_all()
>>> exit()
```

**⚠️ Warning:** `db.drop_all()` will delete all tables and data. Use with extreme caution!

## Running the Application

### 1. Activate Virtual Environment

**On Linux/macOS:**
```bash
source .venv/bin/activate
```

**On Windows:**
```cmd
.venv\Scripts\activate
```

### 2. Start the Flask Development Server

**On Windows:**
```cmd
flask --app process_navigator run --debug
```

**On Linux/macOS:**
```bash
flask --app process_navigator run --debug
```

The application will be available at `http://127.0.0.1:5000/`

### 3. Stop the Server
Press `Ctrl+C` in the terminal to stop the server.

## Development

### Instance Folder
The `instance/` folder is in `.gitignore` and stores instance-specific configuration and data:
- Configuration files (`development_config.py`, `testing_config.py`)
- File uploads (`file_storage/` or `test_file_storage/`)
- Any other instance-specific data

This folder structure allows you to run multiple instances of the app with different configurations.

### Code Formatting
This project uses [Black](https://black.readthedocs.io/) for consistent code formatting.

**Format your code:**
```bash
# Format a specific directory
black process_navigator/

# Format all code
black process_navigator/ tests/

# Check formatting without making changes
black --check process_navigator/ tests/
```

### Custom Flask Commands

#### Refresh Database
The application includes a custom command to refresh the database:

```bash
flask --app process_navigator refresh-database
```

This command will drop all tables and recreate them. **Use with caution** as it deletes all data!

## CI/CD and Testing

This project has automated CI/CD pipelines that run on every push and pull request:

- **Tests Workflow**: Runs the full test suite with coverage reporting
- **Code Quality Workflow**: Checks code formatting with Black

See `.github/workflows/CI_CD_README.md` for detailed documentation.

### Running Tests Locally

With your virtual environment activated:

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=process_navigator --cov-report=html --cov-report=term

# Run specific test file
pytest tests/test_home_routes.py

# Run with verbose output
pytest -v

# Check code formatting (does not modify files)
black --check process_navigator/ tests/

# Format code automatically
black process_navigator/ tests/
```

Coverage reports are generated in the `htmlcov/` directory. Open `htmlcov/index.html` in a browser to view detailed coverage information.

## Troubleshooting

### Database Connection Issues

**Problem:** Cannot connect to PostgreSQL
**Solutions:**
- Verify PostgreSQL is running:
  - Windows: Check Services (Win+R, type `services.msc`)
  - Linux: `sudo systemctl status postgresql`
  - macOS: `brew services list`
- Check your database credentials in `instance/development_config.py`
- Ensure the database exists: `psql -U postgres -l`
- Verify the user has proper permissions

**Problem:** "peer authentication failed" error (Linux)
**Solution:** 
- Edit PostgreSQL's `pg_hba.conf` file
- Change authentication method from `peer` to `md5` for local connections
- Restart PostgreSQL: `sudo systemctl restart postgresql`

### Import Errors

**Problem:** "No module named 'process_navigator'" or similar errors
**Solutions:**
- Ensure your virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
- Check that you're in the project root directory

### Port Already in Use

**Problem:** Flask cannot start because port 5000 is in use
**Solution:** 
- Specify a different port: `flask --app process_navigator run --port 5001 --debug`
- Or find and stop the process using port 5000

### Database Tables Not Created

**Problem:** Tables don't exist when running the application
**Solution:**
- Run the Flask shell and create tables:
  ```bash
  flask --app process_navigator shell
  >>> from process_navigator.extensions.database import db
  >>> db.create_all()
  >>> exit()
  ```

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [pytest Documentation](https://docs.pytest.org/)

## Project Documentation

For more detailed information about the project:
- `PROJECT_PLAN.md` - Project roadmap and feature planning
- `COPILOT_INSTRUCTIONS.md` - Detailed architecture and coding guidelines
- `TESTING_FRAMEWORK.md` - Comprehensive testing documentation
- `.github/workflows/CI_CD_README.md` - CI/CD pipeline documentation

## Future Features
- Database diagram visualization
- API endpoints for external integrations
- Advanced data export and reporting
- Multi-user collaboration features

## License
This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

