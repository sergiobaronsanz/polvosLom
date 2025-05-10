from django.contrib import admin
from .models import TMIc

class TMIcAdmin(admin.ModelAdmin):
    list_display= ('muestra',)



admin.site.register(TMIc, TMIcAdmin)
