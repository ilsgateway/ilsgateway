#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from rapidsms.contrib.handlers.handlers.keyword import KeywordHandler
from ilsgateway.models import ContactDetail, ServiceDeliveryPoint


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
        self.respond("To register, send JOIN <NAME>")

    def handle(self, text):
        name, service_delivery_point_name = text.split()

        try:
            sdp = ServiceDeliveryPoint.objects.filter(name__iexact=service_delivery_point_name)[0:1].get()
        except ServiceDeliveryPoint.DoesNotExist:
            self.respond("Sorry, can't find the location %s" % service_delivery_point_name)
            return
        
        contact = ContactDetail.objects.create(name=name, service_delivery_point=sdp)
        
        self.msg.connection.contact = contact
        self.msg.connection.save()

        self.respond("Thank you for registering at %s, %s" % (service_delivery_point_name, contact.name))