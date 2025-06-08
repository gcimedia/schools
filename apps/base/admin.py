from django.contrib import admin

from .admin_site import org_admin_site
from .forms import OrgDetailForm, OrgGraphicForm, SocialMediaLinkForm
from .models import (
    EmailAddress,
    OrgDetail,
    OrgGraphic,
    PhoneNumber,
    PhysicalAddress,
    SocialMediaLink,
)



@admin.register(OrgDetail, site=org_admin_site)
class OrgDetailAdmin(admin.ModelAdmin):
    form = OrgDetailForm
    list_display = ("name", "value")
    list_editable = ("value",)
    list_filter = ("name",)
    search_fields = ("name", "value")
    ordering = ("name",)
    fieldsets = (
        (
            "Site Detail",
            {
                "fields": (
                    "name",
                    "value",
                )
            },
        ),
    )

    superuser_only_choices = ["org_author", "org_author_url"]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ("name",)
        return ()

    def get_form(self, request, obj=None, **kwargs):
        """Override form to filter superuser-only fields"""
        form = super().get_form(request, obj, **kwargs)

        if not request.user.is_superuser:
            if hasattr(form.base_fields.get("name"), "choices"):
                original_choices = form.base_fields["name"].choices
                # Filter out superuser-only choices
                filtered_choices = [
                    choice
                    for choice in original_choices
                    if choice[0] not in self.superuser_only_choices
                ]
                form.base_fields["name"].choices = filtered_choices

        return form

    def get_queryset(self, request):
        """Filter queryset to hide superuser-only fields from non-superusers"""
        qs = super().get_queryset(request)

        if not request.user.is_superuser:
            # Hide superuser-only records from non-superusers
            qs = qs.exclude(name__in=self.superuser_only_choices)

        return qs

    def has_change_permission(self, request, obj=None):
        """Check if user can change specific org detail"""
        if not super().has_change_permission(request, obj):
            return False

        # If obj exists and user is not superuser, check if it's a restricted field
        if obj and not request.user.is_superuser:
            if obj.name in self.superuser_only_choices:
                return False

        return True

    def has_delete_permission(self, request, obj=None):
        """Check if user can delete specific org detail"""
        if not super().has_delete_permission(request, obj):
            return False

        # If obj exists and user is not superuser, check if it's a restricted field
        if obj and not request.user.is_superuser:
            if obj.name in self.superuser_only_choices:
                return False

        return True


@admin.register(OrgGraphic, site=org_admin_site)
class OrgGraphicAdmin(admin.ModelAdmin):
    form = OrgGraphicForm
    list_display = ("name", "image")
    list_editable = ("image",)
    list_filter = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    fieldsets = (
        (
            "Site Graphic",
            {
                "fields": (
                    "name",
                    "image",
                )
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ("name",)
        return ()


@admin.register(SocialMediaLink, site=org_admin_site)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    form = SocialMediaLinkForm
    list_display = ("name", "url", "is_active", "order")
    list_editable = ("url", "order")
    list_filter = ("is_active", "name")
    search_fields = ("name", "url")
    ordering = ("order", "name")
    fieldsets = (
        (
            "Social Media Details",
            {
                "fields": (
                    "name",
                    "url",
                )
            },
        ),
        ("Display Options", {"fields": ("is_active", "order")}),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ("name",)
        return ()


@admin.register(PhoneNumber, site=org_admin_site)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ("number", "is_active", "is_primary", "use_for_whatsapp", "order")
    list_editable = ("order",)
    list_filter = ("is_active", "is_primary", "use_for_whatsapp")
    search_fields = ("number",)
    ordering = ("order",)
    fieldsets = (
        (
            "Phone Number Details",
            {"fields": ("number",)},
        ),
        (
            "Display Options",
            {"fields": ("is_active", "is_primary", "use_for_whatsapp", "order")},
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ("number",)
        return ()


@admin.register(EmailAddress, site=org_admin_site)
class EmailAddressAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "is_primary", "order")
    list_editable = ("order",)
    list_filter = ("is_active", "is_primary")
    search_fields = ("email",)
    ordering = ("order",)
    fieldsets = (
        (
            "Email Address Details",
            {"fields": ("email",)},
        ),
        ("Display Options", {"fields": ("is_active", "is_primary", "order")}),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ("email",)
        return ()


@admin.register(PhysicalAddress, site=org_admin_site)
class PhysicalAddressAdmin(admin.ModelAdmin):
    list_display = ("label", "city", "country", "is_primary", "is_active", "order")
    list_editable = ("order",)
    list_filter = ("is_active", "is_primary", "country")
    search_fields = ("label", "street_address", "city", "country")
    ordering = ("order",)
    fieldsets = (
        (
            "Address Details",
            {
                "fields": (
                    "label",
                    "building",
                    "street_address",
                    "city",
                    "state_province",
                    "postal_code",
                    "country",
                    "map_embed_url",
                )
            },
        ),
        ("Display Options", {"fields": ("is_active", "is_primary", "order")}),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ("label",)
        return ()
