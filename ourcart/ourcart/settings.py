"""
Django settings for ourcart project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from firebase_admin import initialize_app
import firebase_admin
from firebase_admin import credentials

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p)#@ff)0m1#-=&kje7hifm9ns1e)h!n51!!rouqb&s$pbbi_^!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', '192.168.1.100', '192.168.95.131']



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',
    'rest_framework',
    'rest_framework.authtoken',
    'fcm_django',
    'notification',
  

    
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

ROOT_URLCONF = 'ourcart.urls'

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

WSGI_APPLICATION = 'ourcart.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ourcartstore',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/


FIREBASE_APP = initialize_app()
FCM_DJANGO_SETTINGS = {
    
    "FCM_SERVER_KEY": "AAAAqLW-qYQ:APA91bGc0XJM32KQyb8yIjB47VkiHNKDNazbnxwe5MGz4j2KQEzgbT4pvyHgNCb2xQkpuSw7qKn0TKudQIFLSoBzBcMov07zqK48JE3cu4T_YGHwViL3cCEDFPkyQECvUHtU3yDOq0Qd",
    
    "ONE_DEVICE_PER_USER": False,
   
    "DELETE_INACTIVE_DEVICES": False,
}


STATIC_URL = '/static/'

#STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_DIRS = [(os.path.join(BASE_DIR, 'static'))]
#STATIC_ROOT = BASE_DIR / "static_cdn"

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static_cdn')
STATIC_URL = '/static_cdn/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_cdn'),
]


MEDIA_URL = "/media/"
#MEDIA_ROOT = BASE_DIR / "media"

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

#authentication django api
AUTH_USER_MODEL = 'api.User'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
       
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ]
    
}



REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'users.serializers.UserSerializer',
}
REST_AUTH_REGISTER_SERIALIZERS = {
    "REGISTER_SERIALIZER": "users.serializers.CustomRegisterSerializer",
}







