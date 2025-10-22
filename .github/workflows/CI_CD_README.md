# CI/CD Documentation

This directory contains GitHub Actions workflows for automating testing, code quality checks, and deployment processes.

## Workflows

### 1. Tests (`tests.yml`)

Runs automated tests on every push and pull request to `main` and `develop` branches.

**What it does:**
- Sets up Python 3.12 environment
- Installs all project dependencies
- Automatically formats code with Black before testing
- Runs pytest with coverage reporting
- Generates coverage reports in XML, HTML, and terminal formats
- Uploads coverage to Codecov (requires `CODECOV_TOKEN` secret)
- Stores HTML coverage reports as artifacts for 30 days
- Enforces minimum 50% code coverage threshold

**Trigger events:**
- Push to `main` or `develop` branches
- Pull requests targeting `main` or `develop` branches

**Artifacts:**
- Coverage HTML report (accessible via GitHub Actions UI)

**Requirements:**
- Repository secret `CODECOV_TOKEN` (optional, for Codecov integration)

### 2. Code Quality (`code-quality.yml`)

Checks code formatting compliance using Black.

**What it does:**
- Sets up Python 3.12 environment
- Installs Black code formatter
- Checks that all code in `process_navigator/` and `tests/` follows Black formatting rules

**Trigger events:**
- Push to `main` or `develop` branches
- Pull requests targeting `main` or `develop` branches

**How to fix formatting issues:**
```bash
# Format code automatically
black process_navigator/ tests/

# Check formatting without modifying files
black --check process_navigator/ tests/
```

## Setting Up Codecov (Optional)

To enable code coverage tracking with Codecov:

1. Go to [codecov.io](https://codecov.io) and sign up/login with your GitHub account
2. Add your repository to Codecov
3. Copy the repository upload token
4. In your GitHub repository, go to Settings → Secrets and variables → Actions
5. Create a new secret named `CODECOV_TOKEN` with your token value

Without this token, coverage reports will still be generated and available as artifacts.

## Running Tests Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests with coverage
pytest --cov=process_navigator --cov-report=html --cov-report=term

# View HTML coverage report
# Open htmlcov/index.html in your browser

# Run with minimum coverage threshold
pytest --cov=process_navigator --cov-fail-under=50
```

## Running Code Quality Checks Locally

```bash
# Install Black
pip install black

# Check formatting
black --check process_navigator/ tests/

# Auto-format code
black process_navigator/ tests/
```

## Viewing Workflow Results

1. Go to your repository on GitHub
2. Click the "Actions" tab
3. Select a workflow run to see details
4. Download artifacts (e.g., coverage reports) from successful runs

## Workflow Status Badges

Add these badges to your README.md to show CI/CD status:

```markdown
![Tests](https://github.com/walliscode/ProcessNavigator/workflows/Tests/badge.svg)
![Code Quality](https://github.com/walliscode/ProcessNavigator/workflows/Code%20Quality/badge.svg)
```

## Future Enhancements

Planned additions to the CI/CD pipeline:

- [ ] Automated deployment to staging environment
- [ ] Production deployment pipeline with manual approval
- [ ] Security scanning (Dependabot, CodeQL)
- [ ] Performance testing
- [ ] Docker image building and publishing
- [ ] Database migration testing
- [ ] Integration tests with test database
- [ ] Multi-version Python testing (3.8, 3.9, 3.10, 3.11, 3.12)
- [ ] Automated release notes generation
- [ ] Slack/Discord notifications on workflow failures

## Troubleshooting

### Tests failing locally but passing in CI (or vice versa)

- Check Python version matches (3.12)
- Ensure all dependencies are installed
- Check for environment-specific differences

### Black formatting check fails

Run `black process_navigator/ tests/` to auto-format your code before committing.

### Coverage threshold not met

The workflow requires at least 50% code coverage. Add more tests to increase coverage, or adjust the threshold in `.github/workflows/tests.yml` if appropriate.

### Workflow not triggering

- Ensure you're pushing to `main` or `develop` branches
- Check that workflow files are in `.github/workflows/` directory
- Verify YAML syntax is correct
- Check repository settings → Actions are enabled

## Contributing

When adding new workflows:

1. Create workflow file in `.github/workflows/`
2. Use descriptive names and comments
3. Test workflow locally using tools like [act](https://github.com/nektos/act)
4. Update this README with documentation
5. Consider adding status badges to main README
