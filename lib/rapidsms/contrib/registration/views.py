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
    language = ''
    if req.LANGUAGE_CODE == 'en':
        language = 'English'
    elif req.LANGUAGE_CODE == 'sw':
        language = 'Swahili'
    elif req.LANGUAGE_CODE == 'es':
        language = 'Spanish'        

    sdp_id = req.session.get('current_sdp_id')
    if sdp_id:
		my_sdp = ServiceDeliveryPoint.objects.get(id=sdp_id)
    else:
	    my_sdp = ServiceDeliveryPoint.objects.filter(contactdetail__user__id=req.user.id)[0:1].get()
    
    contact_detail = None
    if pk is not None:
        contact_detail = get_object_or_404(
            ContactDetail, pk=pk)
    cd = ContactDetail.objects.get(user__id=req.user.id)
    allowed_to_edit = True
    if contact_detail:
        allowed_to_edit = cd.allowed_to_edit(contact_detail.service_delivery_point.parent)
    allowed_to_add = cd.allowed_to_edit(my_sdp)

    if req.method == "POST":
        if req.POST["submit"] == "Delete Contact Detail":
            contact_detail.delete()
            return HttpResponseRedirect(
                reverse(registration))

        else:
            form = ContactDetailForm(
                instance=contact_detail,
                service_delivery_point=my_sdp,
                cd=cd,
                data=req.POST)

            if form.is_valid():
                contact = form.save()
                return HttpResponseRedirect(
                    reverse(registration))

    else:
        form = ContactDetailForm(
            instance=contact_detail, 
            service_delivery_point=my_sdp,
            cd=cd)
    return render_to_response(
        "registration/dashboard.html", {
            "facility_contact_detail_table": ContactDetailTable(my_sdp.child_sdps_contacts(), request=req),
            "district_contact_detail_table": ContactDetailTable(my_sdp.contacts(), request=req),
            "region_contact_detail_table": ContactDetailTable(my_sdp.parent.contacts(), request=req),
            "contact_detail_form": form,
            "contact_detail": contact_detail,
            "language": language,
            "my_sdp": my_sdp,
            "allowed_to_edit": allowed_to_edit,
            "allowed_to_add": allowed_to_add
        }, context_instance=RequestContext(req)
    )
