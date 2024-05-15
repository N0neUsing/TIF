"""
Django settings for sistema project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cwc9m+z#ppu8)+@v#$7ci$=w*gae$+%n&gfq6kcsn#59ze(3a3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# settings.py
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SAMESITE = 'Lax'  # Puedes cambiar a 'Strict' en producción si es necesario


CSRF_TRUSTED_ORIGINS = ["https://sistema-delvalle-noneuser.loca.lt", "192.168.0.116", 'http://4ases.noneusers.online', "http://localhost:8000",]
CORS_ALLOWED_ORIGINS = [
    'https://sistema-delvalle-noneuser.loca.lt',
    'http://4ases.noneusers.online',
    'http://localhost:8000',
                        ]


CSRF_COOKIE_SAMESITE = 'Lax'  # 'None' es necesario si tu sitio es accesible desde múltiples dominios
SESSION_COOKIE_SAMESITE = 'Lax'  # Puedes usar 'Strict' o 'Lax' según tus necesidades

# Application definition

INSTALLED_APPS = [
    'inventario.apps.InventarioConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'sslserver',
    'corsheaders',
    'django_extensions',
    'django.contrib.humanize',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'sistema.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'sistema.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tifdb',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


AUTH_USER_MODEL = 'inventario.Usuario' # modelo de usuario
CSRF_TRUSTED_ORIGINS = [    'https://sistema-delvalle-noneuser.loca.lt',
                            'http://4ases.noneusers.online'
                            'http://localhost:8000',]
CORS_ORIGIN_WHITELIST = [
        'https://sistema-delvalle-noneuser.loca.lt',
        'http://4ases.noneusers.online',
        'http://localhost:8000',
]

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {  # Esto capturará los logs de cualquier logger.
            'handlers': ['console'],
            'level': 'DEBUG',  # Puedes ajustar el nivel según sea necesario.
            'propagate': False,
        },
    },
}

LOGIN_URL = '/inventario/login'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    'https://sistema-delvalle-noneuser.loca.lt',
    'http://4ases.noneusers.online',
    'http://localhost:8000',  # Ajusta esto a tu configuración
]
