"""
Django settings for dev project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

from django.contrib.messages import constants as messages

AUTHENTICATION_BACKENDS = (
	'django.contrib.auth.backends.ModelBackend',  # this is default
	'guardian.backends.ObjectPermissionBackend',
)

MESSAGE_TAGS = {
	messages.DEBUG: 'alert-info',
	messages.INFO: 'alert-info',
	messages.SUCCESS: 'alert-success',
	messages.WARNING: 'alert-warning',
	messages.ERROR: 'alert-danger',
}

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rk^6e34%5v@%n%*(@#_6@70d%h+jle#z#ea!iq=o-b9ok@s91#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
GEOIP_PATH = os.path.join(BASE_DIR, '_geoip2_')
INSTALLED_APPS = [
	'trading_system',
	'store',
	'test_app',
	'channels',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'accounts.apps.AccountsConfig',
	'static',
	'templates',
	'guardian',
	'formtools',
	'django_countries',
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

ROOT_URLCONF = 'dev.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(BASE_DIR, 'templates')]
		,
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

WSGI_APPLICATION = 'dev.wsgi.application'
ASGI_APPLICATION = "dev.routing.application"
# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'tradingsystem',
		'USER': 'root',
		'password': '',
		'HOST': 'localhost',
		'PORT': ''
	}
	# 'default': {
	# 	'ENGINE': 'django.db.backends.mysql',
	# 	'NAME': 'tradingsystem',
	# 	'USER': 'tr',
	# 	'password': '',
	# 	'HOST': '132.73.213.227',
	# 	'PORT': ''
	# }
}

redis_host = os.environ.get('REDIS_HOST', 'localhost')
CHANNEL_LAYERS = {
	"default": {
		# This example app uses the Redis channel layer implementation channels_redis
		"BACKEND": "channels_redis.core.RedisChannelLayer",
		"CONFIG": {
			"hosts": [(redis_host, 6379)],
		},

	},
}
# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Jerusalem'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# SESSION_ENGINE = "multi_sessions.session"
LOGIN_REDIRECT_URL = '/login_redirect'
LOGOUT_REDIRECT_URL = '/'
STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATICFILES_DIRS = ["static", ]

MEDIA_URL = '/images/'
MEDIA_ROOT = os.path.join(BASE_DIR, "static/images")

PROJ_IP = '127.0.0.1'
PROJ_PORT = '8000'
# SESSION_MULTISESSIONS_POOL = (
#     {"backend": "redis_sessions.session", "modes": ["read", "write"]},
#     {"backend": "django.contrib.sessions.backends.db", "modes": ["read", "delete"]},
# )

