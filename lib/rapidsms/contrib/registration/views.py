#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from ilsgateway.forms import ContactDetailForm
from ilsgateway.models import ContactDetail, ServiceDeliveryPoint
from ilsgateway.tables import ContactDetailTable
from django.contrib.auth.decorators import login_required

@login_required
def registration(req, pk=None):
    my_sdp = ServiceDeliveryPoint.objects.filter(contactdetail__user__id=req.user.id)[0:1].get()
    contact_detail = None

    if pk is not None:
        contact_detail = get_object_or_404(
            ContactDetail, pk=pk)

    if req.method == "POST":
        if req.POST["submit"] == "Delete Contact Detail":
            contact_detail.delete()
            return HttpResponseRedirect(
                reverse(registration))

        else:
            form = ContactDetailForm(
                instance=contact_detail,
                data=req.POST)

            if form.is_valid():
                contact = form.save()
                return HttpResponseRedirect(
                    reverse(registration))

    else:
        form = ContactDetailForm(
            instance=contact_detail, 
            service_delivery_point=my_sdp)
    print my_sdp
    print my_sdp.child_sdps()
    print my_sdp.child_sdps_contacts()
    return render_to_response(
        "registration/dashboard.html", {
            "contact_detail_table": ContactDetailTable(my_sdp.child_sdps_contacts(), request=req),
            "contact_detail_form": form,
            "contact_detail": contact_detail
        }, context_instance=RequestContext(req)
    )
