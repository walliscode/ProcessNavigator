# GitHub Copilot Instructions for ProcessNavigator

## Project Overview
ProcessNavigator is a Flask-based web application designed to provide a database-driven approach to quantifying physical processes. The application uses PostgreSQL as its database backend and follows a modular architecture with three main components: home, data, and cauldron.

## Tech Stack
- **Backend Framework**: Flask 3.0.3
- **Database**: PostgreSQL with SQLAlchemy 2.0.34 ORM
- **Testing**: pytest 8.3.3
- **Code Formatting**: black 24.8.0
- **Python Version**: 3.8+
- **License**: GNU GPL v3

## Project Structure

```
process_navigator/
├── __init__.py                 # Flask app factory
├── home/                       # User authentication and home pages
│   ├── routes.py
│   └── forms.py
├── data/                       # Data management (inputs, parameters, units, etc.)
│   ├── routes.py
│   └── forms.py
├── cauldron/                   # Process path management
│   ├── routes.py
│   ├── forms.py
│   └── models.py
├── models/                     # SQLAlchemy database models
│   ├── admin.py               # User model
│   ├── process.py             # Process-related models
│   ├── inputs.py              # Input materials
│   ├── parameters.py          # Process parameters
│   ├── units.py               # Units of measurement
│   └── analysis.py            # Analysis methods
├── extensions/                 # Flask extensions
│   ├── database.py            # SQLAlchemy setup
│   └── click.py               # CLI commands
├── utils/                      # Utility functions
│   ├── decorators.py          # Custom decorators
│   └── file_handling.py       # File operations
├── templates/                  # Jinja2 templates
└── static/                     # Static assets (CSS, JS, images)

tests/
├── conftest.py                # pytest fixtures and configuration
├── data/                      # Test data (JSON files)
├── test_*.py                  # Test modules
└── load_data.py               # Test data loading utilities
```

## Key Architectural Patterns

### 1. Flask Blueprints
The application is organized into three main blueprints:
- **home**: User registration, login, and main dashboard
- **data**: CRUD operations for inputs, parameters, units, process methods, and analysis methods
- **cauldron**: Process path creation and management

### 2. Database Models
All models inherit from `Base` (SQLAlchemy declarative base) and use:
- Mapped columns with type hints (`Mapped[type]`)
- Relationships for foreign keys
- Hybrid properties for computed attributes

Example pattern:
```python
class Entity(Base):
    __tablename__ = "entity"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    process_id: Mapped[int] = mapped_column(db.ForeignKey("process.id"))
    process: Mapped["Process"] = relationship("Process", back_populates="entities")
```

### 3. Forms and WTForms
- All forms use Flask-WTF/WTForms
- Forms are defined in module-specific `forms.py` files
- Form validation happens in route handlers

### 4. Session Management
- Custom decorators handle authentication (`@login_required`)
- Session keys track user workflow state (`@session_keys`)
- Security keys list controls page flow

### 5. Instance Folder Pattern
Configuration and instance-specific data (databases, uploads) are stored in the `instance/` folder:
- Development config: `instance/development_config.py`
- Test config: `instance/testing_config.py`
- File storage: `instance/file_storage/` (production) or `instance/test_file_storage/` (testing)

## Coding Conventions

### Python Style
1. **PEP 8 Compliance**: Use `black` for automatic formatting
   ```bash
   black process_navigator/
   ```

2. **Type Hints**: Use type hints for function parameters and return values
   ```python
   def expand_paths(self) -> List[Tuple]:
       # implementation
   ```

3. **Docstrings**: Use descriptive docstrings for modules and complex functions
   ```python
   """Contains sqlalchemy models for the process_navigator app."""
   ```

4. **Naming Conventions**:
   - Classes: PascalCase (e.g., `ProcessMethod`, `PathData`)
   - Functions/methods: snake_case (e.g., `create_app`, `expand_paths`)
   - Constants: UPPER_SNAKE_CASE (e.g., `DATABASE_URI`)
   - Private methods: prefix with underscore (e.g., `_expand_step`)

### Database Conventions
1. **Table Names**: lowercase, singular form (e.g., `entity`, `process`)
2. **Foreign Keys**: Use descriptive names ending in `_id` (e.g., `process_id`, `user_id`)
3. **Relationships**: Use `back_populates` for bidirectional relationships
4. **Migrations**: Use `db.create_all()` for development (production would need Alembic)

### Route Conventions
1. **Method Decorators**: Always specify allowed methods
   ```python
   @bp.route("/process_path", methods=["GET", "POST"])
   ```

2. **Authentication**: Use `@login_required` decorator for protected routes
3. **Session Keys**: Use `@session_keys()` to validate workflow state
4. **Redirects**: Use `url_for()` for internal redirects
   ```python
   return redirect(url_for("cauldron.process_path"))
   ```

### Testing Conventions
1. **Test Organization**: One test file per blueprint (e.g., `test_home_routes.py`)
2. **Fixtures**: Define reusable fixtures in `conftest.py`
3. **Test Data**: Store test data as JSON in `tests/data/`
4. **Schema Validation**: Use JSON schemas to validate test data structure
5. **Test Naming**: Use descriptive names: `test_<module>_<action>_<expected_result>`
   ```python
   def test_register_user(client, route_options, test_app):
       # implementation
   ```

## Common Tasks and Patterns

### Adding a New Database Model
1. Create the model class in the appropriate file under `models/`
2. Import it in `models/__init__.py`
3. Add relationships to related models
4. Run `db.create_all()` in Flask shell to create tables
5. Add test data in `tests/data/test_data.json`
6. Add loading logic in `tests/load_data.py`

### Adding a New Route
1. Define the route in the appropriate blueprint's `routes.py`
2. Create necessary forms in `forms.py`
3. Create the template in `templates/<blueprint>/`
4. Add route to test data in `tests/data/route_options.json`
5. Write tests in `tests/test_<blueprint>_routes.py`

### Working with Forms
1. Define form class inheriting from `FlaskForm`
2. Use WTForms field types (StringField, IntegerField, etc.)
3. Add validators (DataRequired, Email, etc.)
4. Check form submission with `form.<button>.data`
5. Access form data with `form.<field>.data`

Example:
```python
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')
```

### Database Queries
Use SQLAlchemy 2.0 style queries:
```python
# Select single record
user = db.session.execute(
    db.select(User).filter(User.email == email)
).scalar_one()

# Select all records
users = db.session.scalars(db.select(User)).all()

# Add record
db.session.add(new_user)
db.session.commit()
```

### Working with Itertools for Process Combinations
The cauldron module uses `itertools.product` to generate all possible combinations:
```python
from itertools import product

# Generate combinations of inputs and parameters
step_combinations = list(product(input_combinations, parameter_combinations))
```

## Development Workflow

### Initial Setup
1. Install PostgreSQL and create database
2. Create virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Set up database tables: `flask --app process_navigator shell` → `db.create_all()`
5. Run the app: `flask --app process_navigator run --debug`

### Making Changes
1. Activate virtual environment: `.\.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Unix)
2. Make code changes
3. Format code: `black process_navigator/`
4. Run tests: `pytest`
5. Update requirements if needed: `pip freeze > requirements.txt`

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_home_routes.py

# Run specific test
pytest tests/test_home_routes.py::test_register_user

# Run with verbose output
pytest -v
```

## Common Gotchas and Solutions

### 1. Instance Folder Missing
**Problem**: Flask can't find configuration files
**Solution**: Create `instance/` folder and configuration files (not in git)

### 2. Database Connection Issues
**Problem**: Can't connect to PostgreSQL
**Solution**: Check SQLALCHEMY_DATABASE_URI in config, ensure PostgreSQL is running

### 3. Session State Issues
**Problem**: Redirected to wrong page or unauthorized access
**Solution**: Check `security_keys` in session, ensure decorators are in correct order

### 4. Form Validation Failures
**Problem**: Form doesn't validate despite correct input
**Solution**: Check CSRF token, ensure form is properly initialized in template

### 5. Test Database Pollution
**Problem**: Tests fail due to leftover data
**Solution**: Tests use `db.drop_all()` and `db.create_all()` in fixtures to ensure clean state

## Security Considerations

1. **Passwords**: Never store plain text passwords (use hashing)
2. **Session Keys**: Use strong secret keys in production
3. **CSRF Protection**: Enabled by default with Flask-WTF
4. **SQL Injection**: Use SQLAlchemy ORM, never raw SQL with string concatenation
5. **File Uploads**: Validate file types and store in secure location
6. **Environment Variables**: Store sensitive config in environment variables, not in code

## Performance Tips

1. **Database Queries**: Use eager loading with `relationship()` to avoid N+1 queries
2. **Session Management**: Clear unused session data regularly
3. **Static Files**: Serve static files through web server (nginx/Apache) in production
4. **Database Indexing**: Add indexes on frequently queried columns
5. **Caching**: Consider Flask-Caching for expensive operations

## Future Considerations

1. **Migrations**: Add Alembic for database migrations
2. **API**: Consider adding REST API endpoints
3. **Async**: Evaluate async/await for I/O-bound operations
4. **Celery**: Add background task queue for long-running processes
5. **Docker**: Containerize for easier deployment
6. **CI/CD**: Set up automated testing and deployment pipeline

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/)
- [Flask-WTF Documentation](https://flask-wtf.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [Black Documentation](https://black.readthedocs.io/)

## Getting Help

When working on this project with GitHub Copilot:
1. Provide context about which module you're working in
2. Reference existing patterns from similar code
3. Mention any specific conventions to follow
4. Ask for explanations of complex logic (especially in cauldron/models.py)
5. Request tests along with new features
