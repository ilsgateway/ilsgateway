#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from django import forms
from .models import *
from rapidsms.models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ("connections",)