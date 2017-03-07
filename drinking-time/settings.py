import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't=s@n(0=n%l6t@4)zb6b81ec3-*n6zudac05#cf(oe4*tg2&xz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'app'
]

ROOT_URLCONF = 'drinking-time.urls'

WSGI_APPLICATION = 'drinking-time.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR + STATIC_URL

# UTC daterange
DATERANGE = {
    "initial": '12:00:00',
    "final": '21:00:00'
}

SLACK_TOKEN = 'DExnhoykHU2zzB86ux7roUbT'

GIFS = [
    '1.gif',
    '2.gif',
    '3.gif',
    '4.gif',
    '5.gif'
]