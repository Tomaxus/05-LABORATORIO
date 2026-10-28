import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = 'django-insecure-m!(rbpe8c*+z^4znt%s6p4$%-0@0-&06p(n5p&+omly^4a(0f-'

DEBUG = True

ALLOWED_HOSTS: list[str] = []

INSTALLED_APPS = [
    'django_mongodb_backend',
    'devconf.apps.MongoContentTypesConfig',
    'devconf.apps.MongoAuthConfig',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular',
    'corsheaders',
    'django_extensions',
    'devconfsite',
    'cuentas',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True

# HTTPS (Parte 1)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 300  # 5 min: SOLO para el laboratorio
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_REFERRER_POLICY = 'same-origin'
SECURE_CONTENT_TYPE_NOSNIFF = True

# Usuarios de Django sobre MongoDB (Parte 2)
DEFAULT_AUTO_FIELD = 'django_mongodb_backend.fields.ObjectIdAutoField'
MIGRATION_MODULES = {
    'auth': 'mongo_migrations.auth',
    'contenttypes': 'mongo_migrations.contenttypes',
}

JWT_SECRET = os.environ['JWT_SECRET']  # se carga del .env

# El frontend (Next) llega por su proxy desde este origen
CSRF_TRUSTED_ORIGINS = ['https://localhost:3000', 'https://localhost:8443']

ROOT_URLCONF = 'devconf.urls'

WSGI_APPLICATION = 'devconf.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django_mongodb_backend',
        'NAME': os.environ.get('MONGODB_NAME', 'devconf'),
        'HOST': os.environ['MONGODB_URI'],
    },
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}

STATIC_URL = 'static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    },
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    'UNAUTHENTICATED_USER': None,
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'API REST de biblioteca',
    'DESCRIPTION': 'Documentación OpenAPI para libros y editoriales.',
    'VERSION': '1.0.0',
}
