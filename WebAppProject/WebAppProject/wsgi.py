"""
WSGI config for WebAppProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys

sys.path.append("/home/tutalk/cn331-project/WebAppProject")
sys.path.append("/home/tutalk/cn331-project/WebAppProject/WebAppProject")

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebAppProject.settings")

application = get_wsgi_application()
