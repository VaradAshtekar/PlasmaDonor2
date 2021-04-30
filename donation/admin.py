from django.contrib import admin

from .models import Donor, Contact, Centers

admin.site.register(Donor)
admin.site.register(Contact)
admin.site.register(Centers)