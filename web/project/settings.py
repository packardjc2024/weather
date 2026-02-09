"""
"""

import os
from pathlib import Path
import subprocess
from dotenv import load_dotenv
from project.decryption import decrypt_secret


# Set the base directory for the project
BASE_DIR = Path(__file__).resolve().parent.parent

###############################################################################
# Import and decrypt .env values
###############################################################################
SECRETS_PATH = Path.joinpath(BASE_DIR, '.env')
load_dotenv(SECRETS_PATH)
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')

###############################################################################
# Security Settings
###############################################################################
# SECRET_KEY = os.getenv('DJANGO_SECRET')
SECRET_KEY = decrypt_secret(os.getenv("DJANGO_SECRET"), ENCRYPTION_KEY)

# Optionally use /account/ app for login
USE_ACCOUNT = os.getenv("USE_ACCOUNT", "False").strip().lower() == "true"
if USE_ACCOUNT:
    LOGIN_URL = '/account/'
    LOGIN_REDIRECT_URL = '/' # Redirect to home page after logout
    LOGOUT_REDIRECT_URL = '/account/'

DEBUG = True #Bash_Target

USE_SRI = True
SRI_ENABLED = True

###############################################################################
# Django Code
###############################################################################
DOMAIN_NAME = os.getenv('DOMAIN_NAME')

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'weather.programmingondemand.com',
    'www.weather.programmingondemand.com',
]

if DOMAIN_NAME:
    ALLOWED_HOSTS += [
        DOMAIN_NAME,
        f'www.{DOMAIN_NAME}',
    ]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sri',  # Third party for SRI
    'system_check',  # Third party for system checks
    'account',  # My custom login app
    'home_page',  # Home page of app
    'docs',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',
    'project.middleware.CORPMiddleware',  # For CORPS
]

ROOT_URLCONF = 'project.urls'

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
                'project.global_context.add_global_context',  # Loads global context
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

###############################################################################
# Database
###############################################################################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'PORT': os.getenv('DB_PORT'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': decrypt_secret(os.getenv("DB_PASSWORD"), ENCRYPTION_KEY),
        'HOST': os.getenv('DB_HOST'),
    }
}

###############################################################################
# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
###############################################################################
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

###############################################################################
# Internationalization
###############################################################################
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_TZ = True

###############################################################################
# Static files
###############################################################################
STATIC_URL = '/static/' # How to serve static files in templates (source)
MEDIA_URL = '/media/'

FILES_LOCATION = BASE_DIR
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Allow photo/vide uploads due to size (also in nginx file)
DATA_UPLOAD_MAX_MEMORY_SIZE = 10845760

# Security Settings
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

if DEBUG == True:
    SECURE_SSL_REDIRECT = False
else:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    ## Cookie Settings
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    CSRF_COOKIE_SAMESITE = 'Strict'

    # Content Security Policy
    CSP_DEFAULT_SRC = ("'none'", )
    CSP_SCRIPT_SRC = ("'self'",)
    CSP_STYLE_SRC = ("'self'", )
    CSP_IMG_SRC = ("'self'",)
    CSP_FRAME_ANCESTORS = ("'self'",)

    CSP_FONT_SRC = ("'self'",)
    CSP_MEDIA_SRC = ("'self'",)
    CSP_CONNECT_SRC = ("'self'",)


    #Logging
    logger_path = os.path.join(BASE_DIR, 'logs', 'django_logs.txt')
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
            },
            'simple': {
                'format': '%(levelname)s:%(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
            'file': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': logger_path,
                'formatter': 'verbose'
            },
        },
        'loggers': {
            '': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': True,
            },
            'django.request': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': False,
            },
        }
    }

###############################################################################
# Email Settings
###############################################################################
USE_EMAIL = os.getenv("USE_EMAIL", "False").strip().lower() == "true"
if USE_EMAIL:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
    EMAIL_HOST = decrypt_secret(os.getenv("EMAIL_HOST"), ENCRYPTION_KEY)
    EMAIL_USER = decrypt_secret(os.getenv("EMAIL_USER"), ENCRYPTION_KEY)
    EMAIL_PASSWORD = decrypt_secret(os.getenv("EMAIL_PASSWORD"), ENCRYPTION_KEY)
    EMAIL_USE_TLS = True # Use TLS
    EMAIL_USE_SSL = False # Set to False if using TLS on port 587