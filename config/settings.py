import os
from pathlib import Path
from django.urls import reverse_lazy
from celery.schedules import crontab

BASE_DIR = Path(__file__).resolve().parent.parent

# --- .env переменные ---
def getenv_bool(name, default=False):
    return os.getenv(name, str(default)).lower() in ['true', '1', 'yes']

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "!!!-dev-secret-key-!!!")
DEBUG = getenv_bool("DJANGO_DEBUG", True)

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")

# --- Приложения ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_celery_beat",
    # Твои приложения
    "users", "residents", "tasks", "lectures", "references", "reminders",
    "reports", "roles", "storage", "analytics", "notifications",
    # Channels, если используешь
    "channels",
    # CORS (если используешь)
    "corsheaders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # перед CommonMiddleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.global_variables",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.routing.application"  # <--- Важно для Daphne

# --- Redis + Channels ---
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": os.getenv("CHANNEL_LAYERS_BACKEND", "channels_redis.core.RedisChannelLayer"),
        "CONFIG": {
            "hosts": [(os.getenv("CHANNEL_LAYERS_HOST", "redis"), int(os.getenv("CHANNEL_LAYERS_PORT", 6379)))],
        },
    },
}

# --- Celery ---
CELERY_BROKER_URL = f"redis://{os.getenv('REDIS_HOST', 'redis')}:{os.getenv('REDIS_PORT', 6379)}/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"

# --- База данных ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "rehub_db"),
        "USER": os.getenv("POSTGRES_USER", "rehub_user"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "rehub_pass"),
        "HOST": os.getenv("POSTGRES_HOST", "db"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

# --- Пароли ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Язык, время ---
LANGUAGE_CODE = "ru"
TIME_ZONE = "Asia/Almaty"
USE_I18N = True
USE_TZ = True

# --- Статика и медиа ---
STATIC_URL = "/static/"
STATIC_ROOT = os.getenv("STATIC_ROOT", BASE_DIR / "staticfiles")
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.getenv("MEDIA_ROOT", BASE_DIR / "media")

# --- Авторизация ---
AUTH_USER_MODEL = "users.User"
LOGIN_URL = reverse_lazy("users:login")
LOGOUT_URL = reverse_lazy("users:logout")
LOGIN_REDIRECT_URL = reverse_lazy("users:dashboard")
LOGOUT_REDIRECT_URL = reverse_lazy("users:login")

# --- CORS / CSRF ---
def split_and_clean(env_var):
    return [
        origin.strip()
        for origin in os.getenv(env_var, "").split(",")
        if origin.strip().startswith("http://") or origin.strip().startswith("https://")
    ]

CORS_ALLOWED_ORIGINS = split_and_clean("CORS_ALLOWED_ORIGINS")
CSRF_TRUSTED_ORIGINS = split_and_clean("CSRF_TRUSTED_ORIGINS")

# --- Email (если используешь) ---
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = getenv_bool("EMAIL_USE_TLS", True)
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "noreply@rehubpro.kz")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"