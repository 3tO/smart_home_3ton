import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ron%!a5@uh*jscnrjs!9ua8c9ov^fqvnftjhc5fe*sqfsx^i#k'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
