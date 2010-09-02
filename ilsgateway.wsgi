import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

project_root = os.path.abspath(
        os.path.dirname(__file__))

for dir in ["lib", "apps"]:
        path = os.path.join(project_root, dir)
        sys.path.insert(0, path)

sys.path.insert(0, project_root)

sys.path.append('/home/dimagivm/projects')
sys.path.append('/home/dimagivm/projects/ilsgateway')

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
