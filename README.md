# [GCI SCHOOLS MANAGEMENT SYSTEM](https://github.com/gcimedia/schools)

A web application for **Great Commissioners Church International Schools Department**.

## ⚙️ Setup Guide

This guide walks you through setting up the project for both **development** and **production** environments.

### A. 📋 Prerequisites

These apply to **both** development and production setups:

- 🐍 Python 3.13 or higher  
- 📦 Poetry package manager

### B. ⚙️ Poetry Installation

1. Install Poetry using pip:

   ```bash
   pip install poetry
   ```

2. Install dependencies:

   - For **development** (includes dev tools and test libs):

     ```bash
     poetry install
     ```

   - For **production** (excludes dev dependencies):

     ```bash
     poetry install --only main
     ```

### C. 🛠️ Environment Configuration (Production Only)

Set up a `.env` file in your production environment:

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

### D. 🗄️ Database Setup

Same for both development and production:

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

## 📚 System Documentation

- 🧭 [Overview](apps/schools/docs/overview.md)  
- 🗺️ [System Context](apps/schools/docs/system_context.md)  
- 🎯 [System Use Cases](apps/schools/docs/system_use_cases.md)  
- 🗄️ [System Database Design](apps/schools/docs/system_database_design.md)
