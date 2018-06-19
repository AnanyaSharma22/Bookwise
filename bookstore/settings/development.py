from .default import *
DEBUG = True

FB_EMAIL_DOMAIN = r'fbbookwise.com'

FACEBOOK_CONFIG = {
    'app_id': r'1891096117573332',
    'app_secret': r'fc7c7cbd02a4082cc9f2e7f1fbe4eb00',
    'email_domain': FB_EMAIL_DOMAIN
}

FB_TOKEN_URL = 'https://graph.facebook.com/v2.4/me?fields=id,first_name,last_name&access_token='

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_NAME', 'book_wise'),
        'USER':  os.environ.get('DATABASE_USER', 'postgres'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'root'),
        'HOST':  os.environ.get('DATABASE_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DATABASE_PORT', '5432')
    }
}
DEBUG_MAIL = ''


# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'rajan.singh@netsolutions.com'
# EMAIL_HOST_PASSWORD = 'Rajansingh123'
# EMAIL_DEFAULT = 'rajan.singh@netsolutions.com'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ananya.sharma@netsolutions.com'
EMAIL_HOST_PASSWORD = 'ananya@123'
EMAIL_DEFAULT = 'ananya.sharma@netsolutions.com'
DEFAULT_CONTACT_US_EMAIL = 'ananya.sharma@netsolutions.com'

SESSION_COOKIE_HTTPONLY = True
CELERY_ENABLED = False
SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_BROWSER_XSS_FILTER = True

CSRF_COOKIE_HTTPONLY = True

HttpOnly = True
if DEBUG:
    INSTALLED_APPS += [
          'debug_toolbar',
          'mail_panel',
    ]
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware',]
    LST_APP_FOR_LOGGING = ['app', 'accounts', 'oauth2_provider', ]
    INTERNAL_IPS = ['127.0.0.1',]

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'mail_panel.panels.MailToolbarPanel',
    ]
    # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'