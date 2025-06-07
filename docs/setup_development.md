# 🛠️ SETUP DEVELOPMENT

## A. 📋 Prerequisites

- 🐍 Python 3.13 or higher
- 📦 Poetry package manager

## B. Poetry Installation

1. Install Poetry using pip:

```bash
pip install poetry
```

2. Install both main and dev dependencies:

```bash
poetry install
```

## C. Database Setup

1. Create database tables:
```bash
python manage.py makemigrations
python manage.py migrate
```

2. (Optional) Load sample data:
   - 📄 Copy `seed_example.json` from any app's fixtures directory
   - 📝 Create your own fixture file based on the example
   - 📤 Load fixtures using:

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
