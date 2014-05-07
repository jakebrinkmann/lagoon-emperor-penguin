"""
Django settings for espa_web project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$n4y*3o8&@=ldx!ho-(6pe1fqp4&xh6ftlrnj5k#ef%-)q@yis'

# SECURITY WARNING: don't run with debug turned on in production!
#allow us to override this with env var
DEBUG = False
TEMPLATE_DEBUG = False

#make sure its set to a proper value
if os.environ.get('ESPA_DEBUG', '').lower() == 'true':
    DEBUG = True
    TEMPLATE_DEBUG = True


ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ordering',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'espa_web.urls'

WSGI_APPLICATION = 'espa_web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DB_USER = os.environ.get('ESPA_DB_USER', '')
DB_PW   = os.environ.get('ESPA_DB_PW', '')
DB_NAME = os.environ.get('ESPA_DB_NAME', '')
DB_HOST = os.environ.get('ESPA_DB_HOST', '')
DB_PORT = os.environ.get('ESPA_DB_PORT', '')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': DB_NAME,                       # Or path to database file if using sqlite3.
        'USER': DB_USER,                       # Not used with sqlite3.
        'PASSWORD': DB_PW,                     # Not used with sqlite3.
        'HOST': DB_HOST,                       # Set to empty string for localhost. Not used with sqlite3.
        'PORT': DB_PORT,                       # Set to empty string for default. Not used with sqlite3.
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = '/static/'


# Templates

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, "ordering/templates"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.core.context_processors.debug',
	'django.core.context_processors.i18n',
	'django.core.context_processors.media',
	'django.core.context_processors.static',
	'django.contrib.auth.context_processors.auth',
	'django.contrib.messages.context_processors.messages',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)


#ESPA Service URLS

SERVICE_URLS = {
        "dev" : {
            "orderservice":"http://edclxs151.cr.usgs.gov/OrderWrapperServicedevsys/resources",
            "orderdelivery":"http://edclxs151.cr.usgs.gov/OrderDeliverydevsys/OrderDeliveryService?WSDL",
            "orderupdate":"http://edclxs151.cr.usgs.gov/OrderStatusServicedevsys/OrderStatusService?wsdl",
            "massloader":"http://edclxs151.cr.usgs.gov/MassLoaderdevsys/MassLoader?wsdl",
            "registration":"http://edclxs151.cr.usgs.gov/RegistrationServicedevsys/RegistrationService?wsdl"
        },
        "tst" : {
            "orderservice":"http://eedevmast.cr.usgs.gov/OrderWrapperServicedevmast/resources",
            "orderdelivery":"http://edclxs151.cr.usgs.gov/OrderDeliverydevmast/OrderDeliveryService?WSDL",
            "orderupdate":"http://edclxs151.cr.usgs.gov/OrderStatusServicedevmast/OrderStatusService?wsdl",
            #"massloader":"http://edclxs151.cr.usgs.gov/MassLoaderdevmast/MassLoader?wsdl",
            #The tst env for MassLoader is wired to ops because Landsat doesn't usually
            #fulfill test orders unless they are specifically asked to.
            "massloader":"http://edclxs152.cr.usgs.gov/MassLoader/MassLoader?wsdl",
            "registration":"http://edclxs151.cr.usgs.gov/RegistrationServicedevmast/RegistrationService?wsdl"
        },
        "ops" : {
            "orderservice":"http://edclxs152.cr.usgs.gov/OrderWrapperService/resources",
            "orderdelivery":"http://edclxs152.cr.usgs.gov/OrderDeliveryService/OrderDeliveryService?WSDL",
            "orderupdate":"http://edclxs152/OrderStatusService/OrderStatusService?wsdl",
            "massloader":"http://edclxs152.cr.usgs.gov/MassLoader/MassLoader?wsdl",
            "registration":"http://edclxs152.cr.usgs.gov/RegistrationService/RegistrationService?wsdl"
        }
}
