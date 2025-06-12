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

2. **(Optional)** Configure Poetry to create virtualenv inside project roots.

   ```bash
   poetry config.virtualenvs.in-project true
   ```

3. Install dependencies:

   - For **development** (includes dev tools and test libs):

     ```bash
     poetry install
     ```

   - For **production** (excludes dev dependencies):

     ```bash
     poetry install --only main
     ```

### C. 🛠️ Environment Configuration

Set up a `.env` file in your production environment (You can also setup in your development environment, though not required as defaults will be used):

```bash

# Environment (defaults to 'development')
ENVIRONMENT="production"

# Secret Key (defaults to 'Make sure to set your own secret key!')
SECRET_KEY="your-secure-key-here"

# Allowed Hosts (Defaults to 'localhost,127.0.0.1,dev.tawalabora.space')
ALLOWED_HOSTS="localhost,127.0.0.1,example.com,www.example.com"

# Custom App Name (defaults to 'apps.custom')
CUSTOM_APP_NAME="apps.custom"

# Custom App URL Path Configurarion (defaults to 'dashboard/')
CUSTOM_APP_URL="dashboard/"

# Database Configuration (defaults to SQLite3 settings)
DB_POSTGRESQL="True"
DB_SERVICE=""
DB_PASSFILE=""


# Email Configuration (defaults to console backend settings)
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

### E. 📦 Static Files (Production Only)

If you're deploying to production and using a web server (like Nginx) to serve static files, collect them into a single location using:

   ```bash
   python manage.py collectstatic --noinput
   ```

⚠️ This step is not needed in development, as Django serves static files automatically when `DEBUG=True`.

## 📚 System Documentation

- 🧭 [Overview](apps/schools/docs/overview.md)  
- 🗺️ [System Context](apps/schools/docs/system_context.md)  
- 🎯 [System Use Cases](apps/schools/docs/system_use_cases.md)  
- 🗄️ [System Database Design](apps/schools/docs/system_database_design.md)
