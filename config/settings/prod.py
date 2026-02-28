"""
Production settings for config project.
"""

import logging
import os
from pathlib import Path
from django.core.management.utils import get_random_secret_key
from supabase import create_client, Client

# Load environment variables from .env file FIRST
from dotenv import load_dotenv
load_dotenv()

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
# In production, this should be set via environment variables
SECRET_KEY = os.getenv('SECRET_KEY', get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Custom application modules
# INSTALLED_APPS += [
#     'accounts',
# ]

# Configure allowed hosts from environment variable
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Database configuration for production
# Uses environment variables for credentials from Supabase
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME') or os.getenv('DATABASE', 'postgres'),
        'USER': os.getenv('USER', 'postgres'),
        'PASSWORD': os.getenv('PASSWORD', ''),
        'HOST': os.getenv('HOST'),
        'PORT': os.getenv('PORT', '5432'),
        'CONN_MAX_AGE': 600,
            'OPTIONS': {
                'connect_timeout': 10,
            }
    }
}

# Logging configuration for production
# Note: Only use console logging on serverless platforms (Vercel)
# File logging is not suitable for ephemeral environments
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'django': {
        'handlers': ['console'],
        'level': 'INFO',
        'propagate': False,
    },
}

# # Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
}
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# Static files configuration for production
STATIC_URL = '/static/'
# BASE_DIR is the config/ directory; we want project root
STATIC_ROOT = BASE_DIR.parent / 'static'  # collectstatic writes here
STATICFILES_DIRS = []  # no filler dirs needed in production



# Supabase S3 Settings
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'your-access-key-id')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL')

# Public Bucket Specific Settings
AWS_QUERYSTRING_AUTH = False  # Generate clean URLs without expiration tokens
AWS_S3_CUSTOM_DOMAIN = f'duvupolpkzuaqsmhflaw.storage.supabase.co/storage/v1/object/public/{AWS_STORAGE_BUCKET_NAME}'

# Optional: Ensure Django doesn't try to set ACLs (Supabase doesn't support them)
AWS_DEFAULT_ACL = None 

# Set as default storage for media files
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
# MEDIA_URL = f'{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/media/'
MEDIA_URL = ""

MEDIA_ROOT = "" #os.path.join(BASE_DIR, 'media')

# Email configuration for production
EMAIL_BACKEND = os.getenv(
    'EMAIL_BACKEND',
    'django.core.mail.backends.smtp.EmailBackend'
)
EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@propella.com')

# Cache configuration for production
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}


# REST Framework configuration for production
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
    },
}

# CORS configuration for Vercel
# In your CORS_ALLOWED_ORIGINS list, add:
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:8000',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:8000',
    'http://127.0.0.1:7000',
    'http://localhost:5170',      # ADD THIS - Vite default port
    'http://localhost:5173',      # ADD THIS - Vite alternative port
    'http://127.0.0.1:5170',      # ADD THIS
]
if custom_domain := os.getenv('CUSTOM_DOMAIN'):
    CORS_ALLOWED_ORIGINS.append(f'https://{custom_domain}')
if vercel_url := os.getenv('VERCEL_URL'):
    CORS_ALLOWED_ORIGINS.append(f'https://{vercel_url}')

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.vercel\.app$",
]

AUTH_USER_MODEL = 'accounts.User'

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "media")
# Disable admin site in production if desired (comment out to keep it)
# INSTALLED_APPS = [app for app in INSTALLED_APPS if app != 'django.contrib.admin']
