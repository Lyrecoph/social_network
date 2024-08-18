
# Project Overview
This project is a Django-based social network application that includes several features such as user accounts, social interactions, and real-time chat functionality.

![](media/images/screenNetwork1.png)
![](media/images/screenNetwork2.png)
![](media/images/screenNetwork3.png)
![](media/images/screenNetwork4.png)

## Features

**1. User Accounts (accounts):**

Registration, login, and profile management for users.

**2. Social Interactions (social):**

Users can post updates, interact with each other’s content, and receive notifications.

**3. Real-Time Chat (tchat):**

Real-time messaging functionality between users using WebSockets.

## Installation

**1. Clone the repository:**

```bash
git clone https://github.com/Lyrecoph/social_network.git
```

**2. Navigate to the project directory:**

```bash
cd social_network
```

**3. Create a virtual environment:**

```bash
python -m venv venv
```

**4. Activate the virtual environment:**

**On Windows:**

```bash
venv\Scripts\activate
```

**On macOS/Linux:**

```bash
source venv/bin/activate
```

**5. Install dependencies:**

```bash
pip install -r requirements.txt
```

**6. Apply migrations:**

```bash
python manage.py migrate
```

**7. Run the development server:**

```bash
python manage.py runserver
```

## Configuration

Ensure to configure your `settings.py` with the appropriate database settings, `static/media` file settings, and WebSocket configurations.

## WebSocket Setup

WebSockets are used for the real-time chat feature. Ensure your server is configured to support WebSockets. Using channels, follow the necessary setup instructions.

## URLs Configuration

The project has the following URL configurations:

**Admin:** `/admin/`

**Accounts:** `/accounts/`

**Social:** `/social/`

**Chat:** `/tchat/`

## Static and Media Files

Make sure your `STATIC_URL` and `MEDIA_URL` are properly configured. During development, static and media files are served if `DEBUG` is set to `True`.

## .gitignore
Add the following to your `.gitignore` file to ensure sensitive and unnecessary files are not included in your version control:

```bash

# Python
__pycache__/
*.py[cod]
*.sqlite3

# Virtual Environment
venv/
env/
*.venv/

# Django
db.sqlite3
media/
staticfiles/
settings.py

# IDE Specific
.vscode/
.idea/

# OS Specific
.DS_Store
Thumbs.db
```
**settings.example.py**

```
# settings.example.py

import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Placeholder for the Django secret key
SECRET_KEY = 'your-secret-key-here'

# Set to False in production
DEBUG = True

# Add your allowed hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Database configuration (replace placeholders with actual values)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Or another database engine
        'NAME': 'your-database-name',
        'USER': 'your-database-user',
        'PASSWORD': 'your-database-password',
        'HOST': 'localhost',  # Or your database host
        'PORT': '5432',  # Or your database port
    }
}

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Add your apps here
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'your_project_name.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'your_project_name.wsgi.application'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

# Media files (user-uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# Example email configuration (replace with actual values)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.your-email-provider.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-email-password'

# Placeholder for other configurations, like caching, third-party APIs, etc.
```

## Technologies used

This project was carried out using the following technologies:

## Languages

**Python:** Used for backend development with Django.
**Javascript vanilla**: Used for frontend and backend development 

## Backend frameworks

**Django:** Main backend web framework used to build the server, manage the business logic and interact with the database.

## Services

**WebSocket:** Used for real-time chat functionalities.

## Development Tools

**Git :** Used for version control.
**GitHub:** Used for source code hosting and collaboration.
**VS Code:** Main code editor for development.

## Databases

**PostgreSQL:** Relational database used to store application data.

## To-Do List

**1. Social Module:**

- Improve the post-interaction functionalities.
- Implement better notification handling.

**2. Chat Module:**

- Add support for group chats.
- Improve the WebSocket connection stability and error handling.

**3. User Accounts:**

- Add two-factor authentication.
- Enhance profile customization options.

**4. Deployment:**

Set up proper deployment configurations for production (e.g., using `nginx` with `daphne` for WebSocket support).