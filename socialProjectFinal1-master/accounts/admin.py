from django.contrib import admin
from .models import userpermission, permittedlist, resolvedlist
admin.site.register(userpermission)
admin.site.register(permittedlist)
admin.site.register(resolvedlist)
# Register your models here.
