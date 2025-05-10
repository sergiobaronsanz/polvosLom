# en admin.py (donde tengas tu modelo Diminutivo)

# admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Firmas

class FirmaInline(admin.StackedInline):  # También puedes usar TabularInline
    model = Firmas
    can_delete = False
    verbose_name_plural = 'Firma'

class UserAdmin(BaseUserAdmin):
    inlines = (FirmaInline,)
    list_display = ('username', 'email', 'get_firma')

    def get_firma(self, obj):
        return obj.firmas.firma if hasattr(obj, 'firmas') else '(Sin firma)'
    get_firma.short_description = 'Firma'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

