#!/usr/bin/env python

def LoadRegions(in_file):
    print "Loading Regions from %s" % (in_file)
    
    f = open(in_file, 'rU' )
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
        pk = row[0]
        region_name = row[1]
        if region_name == 0:
            continue

        existing_sdp = Region.objects.filter(name=region_name)
        if existing_sdp:
            skipped = skipped + 1
            continue
            
        latitude = 0
        longitude = 0        
        if len(row) > 2:
            longitude = row[2] 
        if len(row) > 3:
            latitude = row[3]
        p = None
        if longitude and longitude != '0' and latitude and latitude != '0':
            p = Point(latitude=latitude, longitude=longitude)
            p.save()
        sdp = Region(pk=pk, point=p, name=row[1], parent_type=ContentType.objects.get_for_model(MinistryOfHealth), parent_id = top_level_sdp.id, service_delivery_point_type_id=2)
        sdp.save()
        print sdp
        count = count + 1
        
    print "Loaded %d new Region(s), skipped %d" % (count, skipped)
        
def LoadDistricts(in_file):
    print "Loading Districts from %s" % (in_file)
    
    f = open(in_file, 'rU' )
    reader = csv.reader( f )
    
    header_row = []
    entries = []
    
    count = 0
    skipped = 0

    for row in reader:
        if not header_row:
            header_row = row
            continue
        district_name = row[2].upper()
        if not district_name or district_name == 0:
            continue

        existing_sdp = District.objects.filter(name=district_name)
        if existing_sdp:
            skipped = skipped + 1
            continue
        
        sdp = District()
        parent_name = row[1].upper()
        parent_regions = ServiceDeliveryPoint.objects.filter(name=parent_name)
        if not parent_regions:
            print "Invalid Region Name: %s" % parent_name
            print "Please correct and retry"
            sys.exit(1)
            
        sdp.parent_id = parent_regions[0].id  
        sdp.parent_type = ContentType.objects.get_for_model(Region)
        sdp.pk = row[0] 
        sdp.name = district_name
        longitude = row[4] 
        latitude = row[5]
        p = None
        if longitude and longitude != '0' and latitude and latitude != '0':
            p = Point(latitude=latitude, longitude=longitude)
            p.save()
        sdp.point = p
        sdp.service_delivery_point_type_id=3
        sdp.save()
        print sdp
        count = count + 1
        
    print "Loaded %d new District(s), skipped %d" % (count, skipped)

def LoadFacilities(in_file):
    print "Loading Facilities from %s" % (in_file)
    
    f = open(in_file, 'rU' )
    reader = csv.reader( f )
    
    header_row = []
    entries = []
    
    count = 0
    skipped = 0
    for row in reader:
        if not header_row:
            header_row = row
            continue
        facility_name = row[4].upper()
        if not facility_name or facility_name == 0:
            continue

        parent_name = row[3].upper()
        parent_districts = District.objects.filter(name=parent_name)
        if not parent_districts:
            print "Invalid District Name: %s" % parent_name
            print "Please correct and retry"
            print row
            sys.exit(1)

        msd_code = row[1].upper()
        if not re.match('D\d+', msd_code):
            print "Invalid MSD code format: %s" % msd_code
            sys.exit(1)

        existing_sdp = Facility.objects.filter(msd_code=msd_code)
        if existing_sdp:
            print "Facility with MSD Code %s already exists - skipping" % msd_code 
            skipped = skipped + 1
            continue
        
        sdp = Facility() 
        sdp.pk = row[0]   
        sdp.parent_id = parent_districts[0].id
        sdp.parent_type = ContentType.objects.get_for_model(District)
            
        sdp.name = facility_name         
        sdp.msd_code = row[1]
        delivery_group_name = row[5].upper()
        delivery_groups = DeliveryGroup.objects.filter(name__iexact=delivery_group_name)
        if not delivery_groups:
            print "Invalid Delivery Group: %s" % delivery_group_name

        sdp.delivery_group = delivery_groups[0]
        
        longitude = 0
        latitude = 0
        if len(row) > 6:
            longitude = row[6] 
        if len(row) > 7:
            latitude = row[7]
        
        p = None
        if longitude and longitude != '0' and latitude and latitude != '0':
            p = Point(latitude=latitude, longitude=longitude)
            p.save()
        sdp.point = p            
        sdp.service_delivery_point_type_id=4
        sdp.save()
        for product in Product.objects.all():
            ActiveProduct.objects.create(product=product, service_delivery_point=sdp)
        print sdp, longitude, latitude
        count = count + 1
        
    print "Loaded %d new Facilities, skipped %d" % (count, skipped)

def LoadSchedules():
    count = 0
    callbacks = ['ilsgateway.callbacks.run_reminders'] 
#                 'ilsgateway.callbacks.district_randr_reminder', 
#                 'ilsgateway.callbacks.facility_delivery_reminder', 
#                 'ilsgateway.callbacks.district_delivery_reminder', 
#                 'ilsgateway.callbacks.district_delinquent_deliveries_summary',
#                 'ilsgateway.callbacks.facility_soh_reminder',]    
    for callback in callbacks: 
        if not EventSchedule.objects.filter(callback=callback):
            e = EventSchedule(callback=callback, 
                              description=callback, 
                              days_of_month='*',
                              hours='*', 
                              minutes=[0,15,30,45])
            e.save()
            count = count + 1
    print "Loaded %d EventSchedules" % count


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

    from ilsgateway.models import ServiceDeliveryPoint, DeliveryGroup, Facility, District, Region, MinistryOfHealth, Product, ActiveProduct
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