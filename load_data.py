#!/usr/bin/env python

def LoadRegions(in_file):
    print "Loading Regions from %s" % (in_file)
    
    f = open(in_file, 'r' )
    reader = csv.reader( f )
    
    header_row = []
    entries = []
    
    top_level_sdp = ServiceDeliveryPoint.objects.filter(name="MOHSW")[0]
    if not top_level_sdp:
        print "Missing initial SDP record - rerun loaddata"
        sys.exit(1)
    count = 0
    skipped = 0
    for row in reader:
        if not header_row:
            header_row = row
            continue
        region_name = row[1]
        if region_name == 0:
            continue

        existing_sdp = ServiceDeliveryPoint.objects.filter(name=region_name)
        if existing_sdp:
            skipped = skipped + 1
            continue
        
        sdp_type = ServiceDeliveryPointType.objects.filter(name__iexact="region")
        if not sdp_type:
            print "Missing Region Service Delivery Point Type - reload initial data with loaddata"
        
        sdp = ServiceDeliveryPoint()
        sdp.parent_service_delivery_point = top_level_sdp            
        sdp.name = row[1]
        sdp.service_delivery_point_type = sdp_type[0]
        print sdp
        sdp.save()
        longitude = row[2] 
        latitude = row[3]
        p = None
        if longitude and longitude != '0' and latitude and latitude != '0':
            p = Point(latitude=latitude, longitude=longitude)
            p.save()
        sdpl = RegionLocation(point=p, service_delivery_point=sdp)
        sdpl.save()        
        count = count + 1
        
    print "Loaded %d new Region(s), skipped %d" % (count, skipped)
        
def LoadDistricts(in_file):
    print "Loading Districts from %s" % (in_file)
    
    f = open(in_file, 'r' )
    reader = csv.reader( f )
    
    header_row = []
    entries = []
    
    count = 0
    skipped = 0

    for row in reader:
        if not header_row:
            header_row = row
            continue
        district_name = row[1].upper()
        if not district_name or district_name == 0:
            continue

        existing_sdp = ServiceDeliveryPoint.objects.filter(name=district_name)
        if existing_sdp:
            skipped = skipped + 1
            continue
        
        sdp = ServiceDeliveryPoint()
        parent_name = row[0].upper()
        parent_regions = ServiceDeliveryPoint.objects.filter(name=parent_name)
        if not parent_regions:
            print "Invalid Region Name: %s" % parent_name
            print "Please correct and retry"
            sys.exit(1)
            
        sdp.parent_service_delivery_point = parent_regions[0]            

        sdp_type = ServiceDeliveryPointType.objects.filter(name__iexact="district")
        if not sdp_type:
            print "Missing District Service Delivery Point Type - reload initial data with loaddata"

        sdp.service_delivery_point_type = sdp_type[0]
        sdp.name = district_name
        print sdp
        sdp.save()
        longitude = row[3] 
        latitude = row[4]
        p = None
        if longitude and longitude != '0' and latitude and latitude != '0':
            p = Point(latitude=latitude, longitude=longitude)
            p.save()
        sdpl = DistrictLocation(point=p, service_delivery_point=sdp)

        parent_sdpls = sdp.parent_service_delivery_point.regionlocation_set.all()
        if not parent_sdpls:
            print sdp, " is missing a parent region location!"

        sdpl.parent_id = parent_sdpls[0].id
        sdpl.parent_type = ContentType.objects.get_for_model(RegionLocation)
        sdpl.save()
        count = count + 1
        
    print "Loaded %d new District(s), skipped %d" % (count, skipped)

def LoadFacilities(in_file):
    print "Loading Facilities from %s" % (in_file)
    
    f = open(in_file, 'r' )
    reader = csv.reader( f )
    
    header_row = []
    entries = []
    
    count = 0
    skipped = 0
    for row in reader:
        if not header_row:
            header_row = row
            continue
        facility_name = row[2].upper()
        if not facility_name or facility_name == 0:
            continue

        parent_name = row[1].upper()
        parent_districts = ServiceDeliveryPoint.objects.filter(name=parent_name)
        if not parent_districts:
            print "Invalid District Name: %s" % parent_name
            print "Please correct and retry"
            print row
            sys.exit(1)

        msd_code = row[0].upper()
        if not re.match('D\d+', msd_code):
            print "Invalid MSD code format: %s" % msd_code
            sys.exit(1)

        existing_sdp = ServiceDeliveryPoint.objects.filter(msd_code=msd_code)
        if existing_sdp:
            print "Facility with MSD Code %s already exists - skipping" % msd_code 
            skipped = skipped + 1
            continue
        
        sdp = ServiceDeliveryPoint()    
        sdp_type = ServiceDeliveryPointType.objects.filter(name__iexact="facility")
        if not sdp_type:
            print "Missing Facility Service Delivery Point Type - reload initial data with loaddata"

        sdp.service_delivery_point_type = sdp_type[0]
        sdp.parent_service_delivery_point = parent_districts[0]            
        sdp.name = facility_name         
        sdp.msd_code = row[0]
        delivery_group_name = row[3].upper()
        delivery_groups = DeliveryGroup.objects.filter(name__iexact=delivery_group_name)
        if not delivery_groups:
            print "Invalid Delivery Group: %s" % delivery_group_name

        sdp.delivery_group = delivery_groups[0]
        sdp.save()
        longitude = row[4] 
        latitude = row[5]
        p = None
        if longitude and longitude != '0' and latitude and latitude != '0':
            p = Point(latitude=latitude, longitude=longitude)
            p.save()            
        sdpl = FacilityLocation(point=p, service_delivery_point=sdp)
        parent_sdpls = sdp.parent_service_delivery_point.districtlocation_set.all()
        if not parent_sdpls:
            print sdp, " is missing a parent district location!"

        sdpl.parent_id = parent_sdpls[0].id
        sdpl.parent_type = ContentType.objects.get_for_model(DistrictLocation)
        sdpl.save()
        count = count + 1
        print sdp, longitude, latitude
        
    print "Loaded %d new Facilities, skipped %d" % (count, skipped)

def LoadSchedules():
    e = EventSchedule(callback="ilsgateway.callbacks.facility_randr_reminder", 
                      description='Facility R&R Reminder', 
                      days_of_month='*',
                      hours=set([1]), 
                      minutes=set([1]))
    e.save()
    
    e = EventSchedule(callback="ilsgateway.callbacks.district_randr_reminder", description='District R&R Reminder', 
                      days_of_month='*',
                      hours=set([1]), 
                      minutes=set([2]))
    e.save()

    e = EventSchedule(callback="ilsgateway.callbacks.facility_delivery_reminder", description='Facility Delivery Reminder', 
                      days_of_month='*',
                      hours=set([1]), 
                      minutes=set([3]))
    e.save()
    print "Loaded EventSchedules"


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

    from ilsgateway.models import ServiceDeliveryPoint, ServiceDeliveryPointType, DeliveryGroup, FacilityLocation, DistrictLocation, RegionLocation
    from django.contrib.contenttypes.models import ContentType
    from rapidsms.contrib.locations.models import Point
    from rapidsms.contrib.scheduler.models import EventSchedule
    
    project_root = os.path.abspath(os.path.dirname(__file__))
    
    import csv
    import re

    model_name = "ServiceDeliveryPoint"
    
    regions_file = os.path.join(project_root, "apps", "ilsgateway", "fixtures", "regions.csv")
    districts_file = os.path.join(project_root, "apps", "ilsgateway", "fixtures", "districts.csv")
    facilities_file = os.path.join(project_root, "apps", "ilsgateway", "fixtures", "facilities.csv")
            
    LoadRegions(regions_file)
    LoadDistricts(districts_file)
    LoadFacilities(facilities_file)
    LoadSchedules()