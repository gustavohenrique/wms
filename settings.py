# -*- coding: utf-8 -*-
import os
PROJECT_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

DEBUG = True
TEMPLATE_DEBUG = True

ADMINS = (
    ('Gustavo','gustavo@gustavohenrique.net'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = os.path.join(PROJECT_ROOT_PATH, 'database.db')  #os.path.join(PROJECT_ROOT_PATH, 'workflow.db')             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

TIME_ZONE = 'America/Sao_Paulo'
LANGUAGE_CODE = 'pt-br'

SITE_ID = 1
USE_I18N = True

MEDIA_ROOT = os.path.join(PROJECT_ROOT_PATH, 'media')
MEDIA_URL = '/media'
#ADMIN_MEDIA_PREFIX = '%s/admin/' % MEDIA_URL
ADMIN_MEDIA_PREFIX = 'http://127.0.0.1:8000/media/admin/'

SECRET_KEY = 'dz*eh@yx!pudxuwogk8)agcf_33&90^llso9(3lqfkgzfa&to9'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'wms.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT_PATH, 'templates')
)

FIXTURE_DIRS = (os.path.join(PROJECT_ROOT_PATH, 'workflow/fixtures'),)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.databrowse',

    'grappelli',
    'django.contrib.admin',
    'geraldo',

    'workflow',
    'client',
    'importer',
    'item',
)

AUTH_PROFILE_MODULE = 'workflow.UserProfile'

LOGIN_URL = 'auth/login/'
LOGOUT_URL = 'auth/logout/'
LOGIN_REDIRECT_URL = '/workflow/'
DATE_FORMAT = '%d/%m/%Y'
DATETIME_FORMAT = 'd/m/Y - H:i:s'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

DATABROWSE_URL='/databrowse/'

