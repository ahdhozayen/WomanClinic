import django_heroku
import os
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR   = os.path.join(BASE_DIR,'womanClinic','templates')
STATIC_DIR      = os.path.join(BASE_DIR,'womanClinic','static')
MEDIA_DIR       = os.path.join(BASE_DIR,'womanClinic','media')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'sn7mr&f%1^$d)72kf3zf*rdm%$s3vye+glj)ja+f3@pf6f(g%)'

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'sn7mr&f%1^$d)72kf3zf*rdm%$s3vye+glj)ja+f3@pf6f(g%)')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost','127.0.0.1','127.0.1.1','64.227.126.140']


# Application definition

INSTALLED_APPS = [
    'custom_user.apps.CustomUserConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'crispy_forms',
    'clinic',
    'home',
    'patient',
    'pharmacy',
    'surgery',
    'report',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'womanClinic.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'womanClinic.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
# 
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'woman_gyno',
        'USER': 'ahd_sysadmin',
        'PASSWORD': 'm@$hreq123',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# Default formats to be used when parsing dates from input boxes, in order
# See all available format string here:
# https://docs.python.org/library/datetime.html#strftime-behavior
# * Note that these format strings are different from the ones to display dates
DATE_INPUT_FORMATS = [
    '%Y-%m-%d', '%d/%m/%Y', '%m/%d/%y',  # '2006-10-25', '25/10/2006', '10/25/06'
    '%b %d %Y', '%b %d, %Y',             # 'Oct 25 2006', 'Oct 25, 2006'
    '%d %b %Y', '%d %b, %Y',             # '25 Oct 2006', '25 Oct, 2006'
    '%B %d %Y', '%B %d, %Y',             # 'October 25 2006', 'October 25, 2006'
    '%d %B %Y', '%d %B, %Y',             # '25 October 2006', '25 October, 2006'
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
LANGUAGE_CODE='ar'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


LANGUAGES = (
    ('en', _('English')),
    ('ar', _('Arabic')),
)


# Languages using BiDi (right-to-left) layout
LANGUAGES_BIDI = ["ar"]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

STATIC_ROOT = '/home/woman_clinic/site/public/static'
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    STATIC_DIR,
    ]
# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files uploaded by user (images etc.)
MEDIA_URL = '/media/'
MEDIA_ROOT = MEDIA_DIR

EXPLORER_CONNECTIONS = {'default': 'default'}
EXPLORER_DEFAULT_CONNECTION = 'default'


AUTH_USER_MODEL = 'custom_user.User'

# Activate Django-Heroku.
django_heroku.settings(locals())
