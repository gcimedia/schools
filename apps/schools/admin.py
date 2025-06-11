from django.contrib import admin

from apps.home.admin_site import portal_site

from .models import School, Unit


@admin.register(School, site=portal_site)
class SchoolAdmin(admin.ModelAdmin):
    pass


@admin.register(Unit, site=portal_site)
class UnitAdmin(admin.ModelAdmin):
    pass
