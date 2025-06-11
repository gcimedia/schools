from django.contrib import admin

from apps.core.admin_site import portal_site

from .models import School, Unit


@admin.register(School, site=portal_site)
class SchoolAdmin(admin.ModelAdmin):
    pass


@admin.register(Unit, site=portal_site)
class UnitAdmin(admin.ModelAdmin):
    pass
