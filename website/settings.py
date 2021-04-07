"""
Django settings for ss project.
Generated by 'django-admin startproject' using Django 3.1.7.
For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
import django_heroku
import dj_database_url


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('secret_key_p8')

# SECURITY WARNING: don't run with debug turned on in production!
if os.environ.get('ENV') == 'PRODUCTION':
    DEBUG = False
else:
    DEBUG = True

ALLOWED_HOSTS = ['https://pure-beurre-th.herokuapp.com/']

# Application definition

INSTALLED_APPS = [
    'product.apps.ProductConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user.apps.UserConfig',

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

ROOT_URLCONF = 'website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 ],
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

WSGI_APPLICATION = 'website.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

if os.environ.get('ENV') == 'PRODUCTION':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'pure_beurre',
            'USER': os.environ.get('username_db_P8'),
            'PASSWORD': os.environ.get('password_db_p8'),
            'HOST': 'localhost',
            'PORT': '5432'
        }
    }
else:
    DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'pure_beurre',
                'USER': os.environ.get('username_db_P8'),
                'PASSWORD': os.environ.get('password_db_p8'),
                'HOST': 'localhost',
                'PORT': '5432'
            }
        }
# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

INTERNAL_IPS = ['127.0.0.1']

if os.environ.get('ENV') == 'PRODUCTION':

    # Static files settings
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')

    STATICFILES_DIRS = (
        os.path.join(PROJECT_ROOT, 'static'),
    )
    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(db_from_env)

CRISPY_TEMPLATE_PACK = 'bootstrap4'
django_heroku.settings(locals())