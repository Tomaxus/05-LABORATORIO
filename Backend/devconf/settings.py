import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


def variable(nombre):
    # falla con un mensaje claro si falta una variable del .env
    try:
        return os.environ[nombre]
    except KeyError:
        raise ImproperlyConfigured(f'Falta la variable {nombre} en el archivo .env (ver .env.example)')


SECRET_KEY = variable('DJANGO_SECRET_KEY')  # distinta a JWT_SECRET

DEBUG = os.environ.get('DEBUG', '0') == '1'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

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
    'cuentas.middleware.CSPMiddleware',
]

# El frontend llega por el proxy de Next (mismo origen); solo se permite su origen
CORS_ALLOWED_ORIGINS = ['https://localhost:3000']
CORS_ALLOW_CREDENTIALS = True

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

JWT_SECRET = variable('JWT_SECRET')

# CSRF (Parte 5)
CSRF_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_HTTPONLY = False  # el frontend debe poder leerla para enviarla en X-CSRFToken
# El frontend (Next) llega por su proxy desde este origen
CSRF_TRUSTED_ORIGINS = ['https://localhost:3000', 'https://localhost:8443']

ROOT_URLCONF = 'devconf.urls'

WSGI_APPLICATION = 'devconf.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django_mongodb_backend',
        'NAME': os.environ.get('MONGODB_NAME', 'devconf'),
        'HOST': variable('MONGODB_URI'),
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

# Errores: detalle solo en la consola del servidor (Parte 6.4)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'consola': {'class': 'logging.StreamHandler'}},
    'loggers': {
        'django': {'handlers': ['consola'], 'level': 'INFO'},
        'cuentas': {'handlers': ['consola'], 'level': 'WARNING'},
    },
}
