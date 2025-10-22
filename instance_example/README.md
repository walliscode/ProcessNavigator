# Instance Configuration Examples

This directory contains example configuration files for the ProcessNavigator application.

## Setup Instructions

1. Create the `instance` directory in the project root if it doesn't exist:
   ```bash
   mkdir instance
   ```

2. Copy the example configuration files:
   ```bash
   # On Linux/macOS:
   cp instance_example/development_config.py instance/
   cp instance_example/testing_config.py instance/

   # On Windows:
   copy instance_example\development_config.py instance\
   copy instance_example\testing_config.py instance\
   ```

3. Edit `instance/development_config.py` to match your local setup:
   - Update the `SECRET_KEY` (generate a secure one for production)
   - Update database credentials if different from defaults
   - Adjust any other settings as needed

## Configuration Files

### development_config.py
Used when running the application in development mode. Contains:
- Database connection string
- Secret key for sessions
- Debug settings

### testing_config.py
Used when running automated tests. Contains:
- In-memory SQLite database (fast, temporary)
- Test-specific settings
- Disabled CSRF protection for easier testing

## Security Notes

- The `instance/` folder is in `.gitignore` and should **never** be committed to version control
- Always use strong, randomly generated secret keys in production
- Never commit passwords or sensitive credentials to the repository
- Consider using environment variables for sensitive data in production environments

## Generating a Secure Secret Key

You can generate a secure random secret key with Python:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and use it as your `SECRET_KEY` in the configuration file.
