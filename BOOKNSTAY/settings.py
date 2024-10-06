import os
import sys
import dj_database_url
#from decouple import config
from pathlib import Path
if os.path.isfile("env.py"):
    import env


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = os.environ.get('SECRET_KEY')

SECRET_KEY = os.getenv('SECRET_KEY', 'SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG =  'DEBUG' in os.environ #os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    '8000-egedegbehenry-booknstay-0bpqw0tupam.ws-eu114.gitpod.io', 
    '127.0.0.1',
    '.herokuapp.com',
    '.gitpod.io',
]

CSRF_TRUSTED_ORIGINS = [
    'https://8000-egedegbehenry-booknstay-0bpqw0tupam.ws-eu114.gitpod.io',
    "https://*.herokuapp.com",
]

# Allow CORS from all origins if set to True
CORS_ALLOW_ALL_ORIGINS = os.getenv('CORS_ALLOW_ALL_ORIGINS', 'True').lower() == 'true'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
     # Django Allauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    #my apps start here
    'hotel',
    'corsheaders',

]

# Middleware configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

# Default message storage backend
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

AUTHENTICATION_BACKENDS = [

    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    
]

ROOT_URLCONF = 'BOOKNSTAY.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
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

WSGI_APPLICATION = 'BOOKNSTAY.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#        }  
#        }

# Fetch the DATABASE_URL and decode it if necessary
database_url = os.getenv("DATABASE_URL")

# Check if database_url is bytes and decode it
if isinstance(database_url, bytes):
    database_url = database_url.decode('utf-8')

# Parse the database URL
DATABASES = {
    'default': dj_database_url.parse(database_url)
}

if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
    
#DATABASES = {"default": dj_database_url.config(default=os.environ.get("DATABASE_URL"))}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

SITE_ID = 1


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'hotel' / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login settings
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'booking_list'
LOGOUT_REDIRECT_URL = '/'

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.example.com'
EMAIL_PORT = 587

EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-email-password'
DEFAULT_FROM_EMAIL = 'webmaster@localhost'


#LOGGING = {
    #"disable_existing_loggers": False,
    #"handlers": {
        #"file": {
            #"level": "DEBUG",
            #"class": "logging.FileHandler",
            #"filename": "/path/to/django/debug.log",
        #},
    #},
    #"loggers": {
       # "django": {
          #  "handlers": ["file"],
          #  "level": "DEBUG",
          #  "propagate": True,
        #},
    #},
#}






