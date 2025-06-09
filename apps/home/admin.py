from django.contrib import admin

from .admin_site import org_admin_site
from .forms import OrgDetailForm, OrgImageForm, SocialMediaLinkForm
from .models import (
    EmailAddress,
    OrgDetail,
    OrgImage,
    PhoneNumber,
    PhysicalAddress,
    SocialMediaLink,
)


class UniqueChoiceAdminMixin(admin.ModelAdmin):
    exclude = ("ordering",)
    list_display = ("name",)
    ordering = ("ordering",)
    superuser_only_choices = []

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if obj:
            readonly_fields.append("name")
        if "ordering" not in readonly_fields:
            readonly_fields.append("ordering")
        return readonly_fields

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser and "name" in form.base_fields:
            form.base_fields["name"].choices = [
                choice
                for choice in form.base_fields["name"].choices
                if choice[0] not in self.superuser_only_choices
            ]
        return form

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.exclude(name__in=self.superuser_only_choices)
        return qs

    def has_add_permission(self, request):
        all_choices = [c[0] for c in self.model.CHOICES]
        if not request.user.is_superuser:
            all_choices = [
                c for c in all_choices if c not in self.superuser_only_choices
            ]
        used = self.model.objects.values_list("name", flat=True)
        remaining = [c for c in all_choices if c not in used]
        return bool(remaining) and super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        if not super().has_change_permission(request, obj):
            return False
        if (
            obj
            and not request.user.is_superuser
            and obj.name in self.superuser_only_choices
        ):
            return False
        return True

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        all_choices = [c[0] for c in self.model.CHOICES]
        if not request.user.is_superuser:
            all_choices = [
                c for c in all_choices if c not in self.superuser_only_choices
            ]
        used = self.model.objects.values_list("name", flat=True)
        extra_context["show_save_and_add_another"] = bool(set(all_choices) - set(used))
        return super().changeform_view(request, object_id, form_url, extra_context)


@admin.register(OrgDetail, site=org_admin_site)
class OrgDetailAdmin(UniqueChoiceAdminMixin):
    form = OrgDetailForm
    list_display = ("name", "value")
    list_editable = ("value",)
    fieldsets = (("Site Detail", {"fields": ("name", "value")}),)
    superuser_only_choices = ["org_author", "org_author_url"]


@admin.register(OrgImage, site=org_admin_site)
class OrgImageAdmin(UniqueChoiceAdminMixin):
    form = OrgImageForm
    list_display = ("name", "image")
    list_editable = ("image",)
    fieldsets = (("Site Graphic", {"fields": ("name", "image")}),)


@admin.register(SocialMediaLink, site=org_admin_site)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    form = SocialMediaLinkForm
    list_display = ("name", "url", "is_active", "order")
    list_editable = ("url", "order")
    list_filter = ("is_active",)
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
    list_display = (
        "label",
        "city",
        "country",
        "use_in_contact_form",
        "is_active",
        "order",
    )
    list_editable = ("order",)
    list_filter = ("is_active", "use_in_contact_form", "country")
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
        ("Display Options", {"fields": ("is_active", "use_in_contact_form", "order")}),
    )
