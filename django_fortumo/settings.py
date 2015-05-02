import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '0_6iq7a%wez2ibbrt07#g&hj1v#pnt9)!^0t)sk3vy72)p%87@'
DEBUG = True
ALLOWED_HOSTS = []

###############################################################################
# Application definition
###############################################################################

INSTALLED_APPS = (
    # core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third party
    'django_nose',

    # internal
    'fortumo',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'django_fortumo.urls'

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

WSGI_APPLICATION = 'django_fortumo.wsgi.application'


###############################################################################
# Database
###############################################################################

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


###############################################################################
# Internationalization
###############################################################################

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


###############################################################################
# Static files (CSS, JavaScript, Images)
###############################################################################

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)


###############################################################################
# Third party
###############################################################################

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'


###############################################################################
# Fortumo
###############################################################################

FORTUMO_ENABLE_IP_VALIDATION = True
FORTUMO_IPS = [
    '127.0.0.1',
    '54.72.6.126',
    '54.72.6.27',
    '54.72.6.17',
    '54.72.6.23',
    '79.125.125.1',
    '79.125.5.205',
    '79.125.5.95',
]
