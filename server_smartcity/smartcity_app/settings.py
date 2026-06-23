from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-4)71(+ncukyyn%n%cb%td_-_-8v&let64@tu8ter!u11)dvh'

DEBUG = True

ALLOWED_HOSTS = ['*']


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

    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',

    # Tambahkan dua baris ini di bawah rest_framework:
    'drf_spectacular',
    'django_scalar',

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


ROOT_URLCONF = 'smartcity_app.urls'


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


WSGI_APPLICATION = 'smartcity_app.wsgi.application'


# =========================================
# DATABASE
# =========================================

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'jujuwita_database',
            'USER': 'postgres',
            'PASSWORD': 'juwitapiuw',
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
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
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

CORS_ALLOW_ALL_ORIGINS = True
STATIC_ROOT = BASE_DIR / 'staticfiles'

# =========================================
# OPENAPI METADATA CONFIG (LAB 14)
# =========================================
SPECTACULAR_SETTINGS = {
    'TITLE': 'Smart City Portal API',  # [cite: 47]
    'DESCRIPTION': 'Dokumentasi REST API resmi untuk Portal Pelaporan Laporan Warga',  # [cite: 48]
    'VERSION': '1.0.0',  # [cite: 49]
    'SERVE_INCLUDE_SCHEMA': False,  # [cite: 50]
}
