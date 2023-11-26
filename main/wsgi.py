"""
WSGI config for main project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

# add the yourdjango project path into the sys.path
sys.path.append('/home/ttt/django/smart_home_3ton/main')

# add the virtualenv site-packages path to the sys.path
sys.path.append('/home/ttt/django/venv/smart_home_3ton/lib/python3.8/site-packages')


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

application = get_wsgi_application()
