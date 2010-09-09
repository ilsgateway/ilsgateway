import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

project_root = os.path.abspath(
        os.path.dirname(__file__))

for dir in ["lib", "apps"]:
        path = os.path.join(project_root, dir)
        sys.path.insert(0, path)

sys.path.insert(0, project_root)

sys.path.append('/home/dimagivm/projects/ilsgateway')
sys.path.append('/home/dimagivm/projects/ilsgateway/apache')

import settings
from logconfig import init_file_logging
init_file_logging(settings.LOG_FILE, settings.LOG_SIZE,
                  settings.LOG_BACKUPS, settings.LOG_LEVEL,
                  settings.LOG_FORMAT)

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
