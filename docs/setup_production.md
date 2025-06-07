# 🚀 SETUP PRODUCTION

## A. 📋 Prerequisites

- 🐍 Python 3.13 or higher
- 📦 Poetry package manager

## B. Environment Configuration

Set up a `.env` file with production values:

```bash
ENVIRONMENT="production"
SECRET_KEY="your-secure-key-here"
ALLOWED_HOSTS="localhost,127.0.0.1,example.com,www.example.com"

# Database Configuration (defaults to SQLite)
DB_ENGINE="django.db.backends.postgresql"
DB_NAME="mydb"
DB_USER="myuser"
DB_PASSWORD="mypassword"
DB_HOST="localhost"
DB_PORT="5432"

# Email Configuration (defaults to console backend)
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST="smtp.gmail.com"
EMAIL_HOST_USER="your-email@gmail.com"
EMAIL_HOST_PASSWORD="your-app-password"
```

## C. Poetry Installation

1. Install Poetry using pip:

```bash
pip install poetry
```

2. Install only main dependencies for production, ignoring dev dependecies:

```bash
poetry install --only main
```

## D. Database Setup

1. Create database tables:
```bash
python manage.py makemigrations
python manage.py migrate
```

2. (Optional) Load sample data:
   - Copy `seed_example.json` from any app's fixtures directory
   - Create your own fixture file based on the example
   - Load fixtures using:
   ```bash
   python manage.py seed
   ```

**Note**: Only `seed_example.json` files are tracked in Git. All other fixture files are gitignored.

## 📚 Guides:

- 🧭 [Index](index.md)
- 🧩 [Overview](overview.md)
- 🗺️ [System Context](system_context.md)
- 🎯 [System Use Cases](system_use_cases.md)
- 🗄️ [System Database Design](system_database_design.md)
- 🛠️ [Setup Development](setup_development.md)
- 🚀 [Setup Production](setup_production.md)
