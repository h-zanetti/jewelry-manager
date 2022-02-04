"""
WSGI config for webdev project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os, sys
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv
from webdev.settings.base import BASE_DIR

dotenv_path = os.path.join(BASE_DIR.parent, '.env')
load_dotenv(dotenv_path)

application = get_wsgi_application()
