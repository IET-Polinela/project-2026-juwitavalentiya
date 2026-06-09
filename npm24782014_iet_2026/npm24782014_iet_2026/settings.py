from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-4)71(+ncukyyn%n%cb%td_-_-8v&let64@tu8ter!u11)dvh'

DEBUG = True

ALLOWED_HOSTS = []


# =========================================
# APPLICATIONS
# =========================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # CORS
    'corsheaders',

    # DRF
    'rest_framework',
    'rest_framework_simplejwt',

    # APPS
    'main_app',
    'about',
    'contacts',
    'usermanagement_24782014',
    'dashboard_24782014',
]


# =========================================
# MIDDLEWARE
# =========================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'corsheaders.middleware.CorsMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'npm24782014_iet_2026.urls'


# =========================================
# TEMPLATES
# =========================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'npm24782014_iet_2026.wsgi.application'


# =========================================
# DATABASE
# =========================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'jujuwita_database',
        'USER': 'postgres',
        'PASSWORD': 'Admin12@',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# =========================================
# AUTH
# =========================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTH_USER_MODEL = 'usermanagement_24782014.CustomUser'


# =========================================
# INTERNATIONALIZATION
# =========================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# =========================================
# STATIC
# =========================================
STATIC_URL = 'static/'


# =========================================
# LOGIN SYSTEM (WEB)
# =========================================
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'


# =========================================
# DRF + JWT CONFIG (LAB 10)
# =========================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}


# =========================================
# DEFAULT AUTO FIELD
# =========================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =========================================
# CORS CONFIG (LAB 11)
# =========================================
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]