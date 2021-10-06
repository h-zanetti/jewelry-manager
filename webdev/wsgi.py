"""
WSGI config for webdev project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os, sys
from django.core.wsgi import get_wsgi_application

# add django project path into the sys.path
sys.path.append('/home/agah/repositories/jewelry-manager')

# add the virtualenv site-packages path to the sys.path
sys.path.append('/home/agah/repositories/jewelry-manager/.venv/lib/python3.9/site-packages')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webdev.settings.development')

application = get_wsgi_application()
