# Helpful Commands Cheat Sheet

Save this for quick reference when working with your Django project.

## Activation & Setup

```bash
# Navigate to project
cd "c:\Users\wowde\Documents\software engineer\school projects\Capstone"

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Deactivate virtual environment
deactivate

# Install packages from requirements
pip install -r requirements.txt

# Install specific package
pip install package_name
```

## Running the Server

```bash
# Start development server (default: http://localhost:8000)
python manage.py runserver

# Start on specific port
python manage.py runserver 8080

# Start and allow external connections
python manage.py runserver 0.0.0.0:8000
```

## Database Management

```bash
# Check for new model changes
python manage.py makemigrations

# Apply all pending migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations

# Create new migration for specific app
python manage.py makemigrations pages

# Reverse (undo) most recent migration
python manage.py migrate pages 0001

# Completely reset database (WARNING: deletes all data!)
python manage.py flush

# Delete all data but keep structure
python manage.py shell -c "
from pages.models import Event, Service, TradePost
Event.objects.all().delete()
Service.objects.all().delete()
TradePost.objects.all().delete()
"
```

## User Management

```bash
# Create superuser (admin account)
python manage.py createsuperuser

# Create regular user (requires superuser account)
python manage.py shell -c "
from django.contrib.auth.models import User
User.objects.create_user('username', 'email@example.com', 'password')
"

# Change user password
python manage.py changepassword username

# Check if user exists
python manage.py shell -c "
from django.contrib.auth.models import User
print(User.objects.filter(username='admin').exists())
"

# Delete user
python manage.py shell -c "
from django.contrib.auth.models import User
User.objects.filter(username='username').delete()
"
```

## Django Shell (Interactive Python)

```bash
# Open Django shell
python manage.py shell

# Inside shell, useful commands:
from django.contrib.auth.models import User
from pages.models import Event, Service, TradePost

# Query examples
users = User.objects.all()
events = Event.objects.filter(event_type='tournament')
posts = TradePost.objects.filter(author=user)

# Create example
event = Event.objects.create(
    title="Test Event",
    description="Test",
    event_type="tournament",
    start_date="2026-02-15 18:00:00",
    end_date="2026-02-15 21:00:00",
    location="Store"
)

# Update
event.title = "Updated Title"
event.save()

# Delete
event.delete()

# Exit shell
exit()
```

## Static Files

```bash
# Collect all static files (needed for production)
python manage.py collectstatic

# Clear static files
python manage.py collectstatic --clear

# Find static file
python manage.py findstatic filename.css
```

## Testing

```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test pages

# Run specific test class
python manage.py test pages.tests.EventTestCase

# Run with verbose output
python manage.py test --verbosity=2
```

## Useful Debugging

```bash
# Show all registered URLs
python manage.py show_urls

# Check Django configuration
python manage.py check

# List installed apps
python manage.py shell -c "
from django.conf import settings
for app in settings.INSTALLED_APPS:
    print(app)
"

# Database query logging
python manage.py shell -c "
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as queries:
    list(Event.objects.all())
    for q in queries:
        print(q['sql'])
"
```

## File Operations

```bash
# Create media folders
mkdir media
mkdir media/trade_posts

# Backup database
copy db.sqlite3 db.sqlite3.backup

# Restore database from backup
copy db.sqlite3.backup db.sqlite3
```

## Common Workflows

### Adding a New Model Feature

```bash
# 1. Edit models.py (pages/models.py)
# 2. Create migration
python manage.py makemigrations

# 3. Apply migration
python manage.py migrate

# 4. Register in admin (pages/admin.py) if needed
# 5. Restart server
```

### Deploying Changes

```bash
# 1. Make changes to code
# 2. Create migrations
python manage.py makemigrations

# 3. Test locally
python manage.py runserver
# (test in browser)

# 4. Apply migrations
python manage.py migrate

# 5. Collect static files
python manage.py collectstatic

# 6. Restart server on production
```

### Resetting Everything

```bash
# 1. Delete database
del db.sqlite3

# 2. Delete migrations (except __init__.py)
# Remove files in pages/migrations/ except __init__.py

# 3. Recreate migrations
python manage.py makemigrations

# 4. Migrate
python manage.py migrate

# 5. Create new superuser
python manage.py createsuperuser
```

## Environment Variables

```bash
# Create .env file (optional)
# Add to project for sensitive data:
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# To use in settings.py, install django-environ:
pip install django-environ
```

## Package Management

```bash
# Show installed packages
pip list

# Show specific package info
pip show Django

# Update package
pip install --upgrade Django

# Uninstall package
pip uninstall package_name

# Export current environment
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt
```

## Troubleshooting Commands

```bash
# Check if server is running
# (usually http://localhost:8000)

# Find process using port 8000
netstat -ano | findstr :8000

# Kill process using port (replace PID)
taskkill /PID 12345 /F

# Clear Python cache
python -Bc "import py_compile; py_compile.compile('filename.py')"

# Check Python version
python --version

# Verify Django installation
python -c "import django; print(django.get_version())"
```

## Quick Admin Tasks

```bash
# Create 10 test events
python manage.py shell << EOF
from pages.models import Event
from datetime import datetime, timedelta
for i in range(10):
    Event.objects.create(
        title=f"Event {i+1}",
        description="Test",
        event_type="tournament",
        start_date=datetime.now() + timedelta(days=i),
        end_date=datetime.now() + timedelta(days=i, hours=3),
        location="Store"
    )
print("Created 10 events")
EOF

# Delete all trading posts
python manage.py shell -c "
from pages.models import TradePost
TradePost.objects.all().delete()
print('All posts deleted')
"

# Make user admin
python manage.py shell -c "
from django.contrib.auth.models import User
user = User.objects.get(username='username')
user.is_staff = True
user.is_superuser = True
user.save()
print('User is now admin')
"
```

## VS Code Integration

```bash
# Format code (requires black)
pip install black
black .

# Lint code (requires pylint)
pip install pylint
pylint pages/

# Type checking (requires mypy)
pip install mypy
mypy pages/
```

## Tips

- **Always backup** `db.sqlite3` before major changes
- **Use `python manage.py check`** to validate configuration
- **Activate venv** before running ANY command
- **Close server** (Ctrl+C) before migrations
- **Keep requirements.txt** updated with `pip freeze`
- **Test locally** before making changes to production

## Emergency Commands

```bash
# If everything breaks, reset everything:
del db.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
# Now create new admin and test

# If stuck in migration errors:
python manage.py migrate --fake pages 0001
python manage.py showmigrations pages
# Then delete problematic migration file and recreate
```

---

**Pro Tip**: Bookmark this file for quick reference when developing!
