from django.contrib import admin

from apps.home.admin_site import org_admin_site

from .models import Module, School


@admin.register(School, site=org_admin_site)
class SchoolAdmin(admin.ModelAdmin):
    pass


@admin.register(Module, site=org_admin_site)
class ModuleAdmin(admin.ModelAdmin):
    pass
