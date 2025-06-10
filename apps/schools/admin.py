from django.contrib import admin

from apps.home.admin_site import admin_site

from .models import School, Unit


@admin.register(School, site=admin_site)
class SchoolAdmin(admin.ModelAdmin):
    pass


@admin.register(Unit, site=admin_site)
class UnitAdmin(admin.ModelAdmin):
    pass
