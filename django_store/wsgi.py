"""
Конфигурация WSGI для проекта django_store.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_store.settings")

application = get_wsgi_application()
