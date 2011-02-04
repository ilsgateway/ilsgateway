PROJECT_NAME = "ILSGateway"

DEFAULT_BACKEND = 'push_backend'

DEBUG = True

MAP_DEFAULT_LATITUDE  = '-10.275059'
MAP_DEFAULT_LONGITUDE = '40.183868'

MONTHS_OF_STOCK_MIN=3
MONTHS_OF_STOCK_MAX=7

LANGUAGES = (
  ('sw', _('Swahili')),
  ('en', _('English')),
)

LANGUAGE_CODE = 'sw'

# Options: PRODUCTION | TEST
ROUTER_MODE="TEST"

TIME_ZONE = "Africa/Dar_es_Salaam"

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',    # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 's$
        'NAME':     'ilsgateway',                                # Or path to database file if using sqlite$
        'USER':     'postgres',                                  # Not used with sqlite3.
        'PASSWORD': 'qsczse',                                    # Not used with sqlite3.
        'HOST':     '',                                          # Set to empty string for localhost. Not u$
        'PORT':     '',                                          # Set to empty string for default. Not use$
    }
}

ADMINS = (('Ryan', 'rhartford@dimagi.com'))
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER  = "ilsgateway@gmail.com"
EMAIL_HOST_PASSWORD = "1lsgat3way"
SERVER_EMAIL = "ilsgateway@gmail.com"
