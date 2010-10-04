
from django.core.management import execute_manager
import sys, os    


os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

try:
    import settings # Assumed to be in the same directory.
except ImportError:
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r." % __file__)    
    sys.exit(1)

if __name__ == "__main__":
    import os
    project_root = os.path.abspath(os.path.dirname(__file__))
    for dir in ["lib", "apps"]:
        path = os.path.join(project_root, dir)
        sys.path.insert(0, path)
    sys.path.insert(0, project_root)

    from ilsgateway.models import ServiceDeliveryPoint, DeliveryGroup, Facility, District, Region, MinistryOfHealth
    from django.contrib.contenttypes.models import ContentType
    from rapidsms.contrib.locations.models import Point
    from rapidsms.contrib.scheduler.models import EventSchedule
    
    project_root = os.path.abspath(os.path.dirname(__file__))
    
    from django.core.management import call_command 
    call_command('syncdb', interactive=False)
    call_command('migrate', 'ilsgateway')
    os.system('python load_data.py')
     