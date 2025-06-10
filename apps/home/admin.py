from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as DjangoGroupAdmin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .admin_site import admin_site
from .forms import BaseDetailForm, BaseImageForm, SocialMediaLinkForm, UserChangeForm
from .models import (
    BaseDetail,
    BaseImage,
    EmailAddress,
    PhoneNumber,
    PhysicalAddress,
    SocialMediaLink,
    User,
    UserGroup,
)


class UniqueChoiceAdminMixin(admin.ModelAdmin):
    """
    Mixin for Django admin models where the 'name' field is chosen from a unique set of
    predefined choices. This mixin restricts non-superusers from selecting or modifying
    certain 'superuser-only' choices, enforces read-only fields on editing, and disables deletion.
    """

    exclude = ("ordering",)
    list_display = ("name",)
    ordering = ("ordering",)
    superuser_only_choices = []

    def get_readonly_fields(self, request, obj=None):
        """
        Returns a list of fields to be displayed as read-only in the admin form.
        The 'name' field is read-only when editing an existing object.
        The 'ordering' field is always read-only.
        """
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if obj:
            readonly_fields.append("name")
        if "ordering" not in readonly_fields:
            readonly_fields.append("ordering")
        return readonly_fields

    def get_form(self, request, obj=None, **kwargs):
        """
        Customize the form to filter out choices from the 'name' field
        that are restricted to superusers only, for non-superuser requests.
        """
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser and "name" in form.base_fields:
            form.base_fields["name"].choices = [
                choice
                for choice in form.base_fields["name"].choices
                if choice[0] not in self.superuser_only_choices
            ]
        return form

    def get_queryset(self, request):
        """
        Modify the queryset to exclude objects with names restricted to superusers
        for non-superuser users.
        """
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.exclude(name__in=self.superuser_only_choices)
        return qs

    def has_add_permission(self, request):
        """
        Determines if the user has permission to add new objects.
        Non-superusers can only add objects with 'name' choices that are not
        restricted to superusers and that are not already used.
        """
        all_choices = [c[0] for c in self.model.CHOICES]
        if not request.user.is_superuser:
            all_choices = [
                c for c in all_choices if c not in self.superuser_only_choices
            ]
        used = self.model.objects.values_list("name", flat=True)
        remaining = [c for c in all_choices if c not in used]
        return bool(remaining) and super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        """
        Disable delete permission for all users.
        """
        return False

    def has_change_permission(self, request, obj=None):
        """
        Restrict change permission such that:
        - Only superusers can edit objects with superuser-only names.
        - Otherwise, follow the default permission logic.
        """
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
        """
        Customize the change form view to conditionally show the 'Save and add another'
        button based on whether there are any remaining allowed choices to add.
        """
        extra_context = extra_context or {}
        all_choices = [c[0] for c in self.model.CHOICES]
        if not request.user.is_superuser:
            all_choices = [
                c for c in all_choices if c not in self.superuser_only_choices
            ]
        used = self.model.objects.values_list("name", flat=True)
        extra_context["show_save_and_add_another"] = bool(set(all_choices) - set(used))
        return super().changeform_view(request, object_id, form_url, extra_context)


@admin.register(BaseDetail, site=admin_site)
class BaseDetailAdmin(UniqueChoiceAdminMixin):
    """
    Admin interface for OrgDetail model, using UniqueChoiceAdminMixin to enforce unique
    'name' choices and restrictions. Allows editing of the 'value' field inline.
    """

    form = BaseDetailForm
    list_display = ("name", "value")
    list_editable = ("value",)
    fieldsets = (("Site Detail", {"fields": ("name", "value")}),)
    superuser_only_choices = ["base_author", "base_author_url", "base_theme_color"]


@admin.register(BaseImage, site=admin_site)
class BaseImageAdmin(UniqueChoiceAdminMixin):
    """
    Admin interface for OrgImage model, using UniqueChoiceAdminMixin to enforce unique
    'name' choices. Allows editing of the 'image' field inline.
    """

    form = BaseImageForm
    list_display = ("name", "image")
    list_editable = ("image",)
    fieldsets = (("Site Graphic", {"fields": ("name", "image")}),)


@admin.register(SocialMediaLink, site=admin_site)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    """
    Admin interface for SocialMediaLink model, supporting listing, filtering, searching,
    and inline editing of URLs and order. Restricts the 'name' field to read-only on edit.
    """

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
        """
        Make the 'name' field read-only when editing an existing SocialMediaLink.
        """
        if obj:  # editing an existing object
            return ("name",)
        return ()


@admin.register(PhoneNumber, site=admin_site)
class PhoneNumberAdmin(admin.ModelAdmin):
    """
    Admin interface for PhoneNumber model with support for listing, filtering,
    searching, ordering, and inline editing of the 'order' field.
    The 'number' field is read-only when editing an existing object.
    """

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
        """
        Make the 'number' field read-only when editing an existing PhoneNumber.
        """
        if obj:  # editing an existing object
            return ("number",)
        return ()


@admin.register(EmailAddress, site=admin_site)
class EmailAddressAdmin(admin.ModelAdmin):
    """
    Admin interface for EmailAddress model with support for listing, filtering,
    searching, ordering, and inline editing of the 'order' field.
    The 'email' field is read-only when editing an existing object.
    """

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
        """
        Make the 'email' field read-only when editing an existing EmailAddress.
        """
        if obj:  # editing an existing object
            return ("email",)
        return ()


@admin.register(PhysicalAddress, site=admin_site)
class PhysicalAddressAdmin(admin.ModelAdmin):
    """
    Admin interface for PhysicalAddress model supporting listing, filtering,
    searching, ordering, and displaying detailed address fields.
    """

    list_display = (
        "label",
        "city",
        "country",
        "use_in_contact_form",
        "is_active",
        "order",
    )
    list_editable = ("order",)
    list_filter = ("is_active", "use_in_contact_form", "country", "state_province")
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


@admin.register(UserGroup, site=admin_site)
class UserGroupAdmin(DjangoGroupAdmin):
    def get_readonly_fields(self, request, obj=None):
        # Make 'name' readonly if the group is protected
        if obj:
            return ["name"] + list(self.readonly_fields)
        return self.readonly_fields


@admin.register(User, site=admin_site)
class UserAdmin(DjangoUserAdmin):
    form = UserChangeForm
    list_display = ["username", "first_name", "last_name", "get_role_for_admin"]
    list_filter = ("is_active", "groups")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "is_superuser", "groups")},
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    def get_role_for_admin(self, obj):
        try:
            return obj.get_role()
        except Exception:
            return "Unknown"

    get_role_for_admin.short_description = "Role"
    get_role_for_admin.admin_order_field = "groups"

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)

        if request.user.is_superuser:
            return fieldsets

        fieldsets = list(fieldsets)
        for name, section in fieldsets:
            section["fields"] = tuple(
                field
                for field in section["fields"]
                if field not in ["is_superuser", "is_staff"]
            )

        return fieldsets
