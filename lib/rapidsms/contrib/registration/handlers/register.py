#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from rapidsms.contrib.handlers.handlers.keyword import KeywordHandler
from ilsgateway.models import ContactDetail, ServiceDeliveryPoint, ContactRole
import string
import re


class RegisterHandler(KeywordHandler):
    """
    Allow remote users to register themselves, by creating a Contact
    object and associating it with their Connection. For example::

        >>> RegisterHandler.test('join Adam Mckaig')
        ['Thank you for registering, Adam Mckaig!']

        >>> Contact.objects.filter(name="Adam Mckaig")
        [<Contact: Adam Mckaig>]

    Note that the ``name`` field of the Contact model is not constrained
    to be unique, so this handler does not reject duplicate names. If
    you wish to enforce unique usernames or aliases, you must extend
    Contact, disable this handler, and write your own.
    """

    keyword = "register|reg|join"

    def help(self):
        self.respond("To register, send register <name> <msd code>. example: register john patel d34002")

    def handle(self, text):
        words = text.split()
        name = []
        msd_code = []
        for the_string in words:
            if re.match('^d\d+', the_string.strip().lower()):
                msd_code.append(the_string.strip().lower())
            else:
                name.append(the_string)
        name = string.join(name, ' ') 
        msd_code = string.join(msd_code, '')
        
        if not msd_code:
            self.respond("To register, send register <name> <msd code>.  You didn't include an msd code. example: register john patel d34002")
            return
        else:            
            try:
                sdp = ServiceDeliveryPoint.objects.filter(msd_code__iexact=msd_code)[0:1].get()
            except ServiceDeliveryPoint.DoesNotExist:
                self.respond("Sorry, can't find the location with MSD CODE %s" % msd_code)
                return
        
        #Default to Facility in-charge for now
        role = ContactRole.objects.filter(name="Facility in-charge")[0:1].get()
        is_primary = True
        if ContactDetail.objects.filter(primary=True, service_delivery_point=sdp):
            is_primary = False
            
        contact = ContactDetail.objects.create(name=name, service_delivery_point=sdp, role=role, primary=is_primary, language="sw")
        
        self.msg.connection.contact = contact
        self.msg.connection.save()

        self.respond("Thank you for registering at %s, %s, %s" % (sdp.name, msd_code, contact.name))