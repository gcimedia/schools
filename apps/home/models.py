import logging

from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

logger = logging.getLogger(__name__)


class UniqueChoiceBaseModel(models.Model):
    """
    Abstract base model for models with a unique 'name' choice field,
    customizable display ordering, and timestamp tracking.
    """

    name = models.CharField(max_length=25, unique=True)
    ordering = models.PositiveIntegerField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    CHOICES = []  # Override in subclass
    ORDER_MAPPING = {}  # Override in subclass

    class Meta:
        abstract = True
        ordering = ["ordering"]

    def save(self, *args, **kwargs):
        """
        Assigns ordering based on ORDER_MAPPING before saving.
        Defaults to 999 if not found.
        """
        if self.name:
            self.ordering = self.ORDER_MAPPING.get(self.name, 999)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_name_display()

    @property
    def display_name(self):
        """Returns the human-readable name of the item"""
        return self.get_name_display()


class BaseDetail(UniqueChoiceBaseModel):
    """
    Represents a customizable organization text detail, such as name, motto,
    theme color, or URLs.
    """

    CHOICES = [
        ("base_name", "Name"),
        ("base_description", "Motto / Description"),
        ("base_theme_color", "Theme Color"),
        ("base_url", "Website URL"),
        ("base_author", "Author's Name"),
        ("base_author_url", "Author's Website URL"),
    ]
    ORDER_MAPPING = {key: i + 1 for i, (key, _) in enumerate(CHOICES)}

    name = models.CharField(max_length=25, choices=CHOICES, unique=True)
    value = models.CharField(
        max_length=255, blank=True, help_text="Value for the organization detail."
    )


class BaseImage(UniqueChoiceBaseModel):
    """
    Represents organization-related image assets like logos, favicons,
    and hero images.
    """

    CHOICES = [
        ("base_logo", "Logo"),
        ("base_favicon", "Favicon"),
        ("base_apple_touch_icon", "Apple touch icon"),
        ("base_hero_image", "Hero / cover image"),
    ]
    ORDER_MAPPING = {key: i + 1 for i, (key, _) in enumerate(CHOICES)}

    name = models.CharField(max_length=25, choices=CHOICES, unique=True)
    image = models.ImageField(
        upload_to="home/base",
        null=True,
        blank=True,
        help_text="Image file for logos, favicons, etc.",
    )


class SocialMediaLink(models.Model):
    """
    Represents a social media link with associated Bootstrap icon class,
    display status, and display order.
    """

    class Meta:
        ordering = ["order", "name"]

    SOCIAL_MEDIA_CHOICES = [
        ("facebook", "Facebook"),
        ("twitter", "X (formerly Twitter)"),
        ("instagram", "Instagram"),
        ("linkedin", "LinkedIn"),
        ("youtube", "YouTube"),
        ("tiktok", "TikTok"),
        ("pinterest", "Pinterest"),
        ("snapchat", "Snapchat"),
        ("discord", "Discord"),
        ("telegram", "Telegram"),
        ("github", "GitHub"),
        ("reddit", "Reddit"),
        ("twitch", "Twitch"),
    ]

    ICON_MAPPING = {
        "facebook": "bi bi-facebook",
        "twitter": "bi bi-twitter-x",
        "instagram": "bi bi-instagram",
        "linkedin": "bi bi-linkedin",
        "youtube": "bi bi-youtube",
        "tiktok": "bi bi-tiktok",
        "pinterest": "bi bi-pinterest",
        "snapchat": "bi bi-snapchat",
        "discord": "bi bi-discord",
        "telegram": "bi bi-telegram",
        "github": "bi bi-github",
        "reddit": "bi bi-reddit",
        "twitch": "bi bi-twitch",
    }

    name = models.CharField(max_length=20, choices=SOCIAL_MEDIA_CHOICES, unique=True)
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Bootstrap icon class (auto-populated based on name)",
    )
    url = models.URLField(help_text="URL to your selected social media profile")
    is_active = models.BooleanField(
        default=True, help_text="Whether this social media link should be displayed"
    )
    order = models.PositiveIntegerField(
        default=0, help_text="Display order (lower numbers appear first)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """Auto-assign icon based on the platform name before saving."""
        if self.name in self.ICON_MAPPING:
            self.icon = self.ICON_MAPPING[self.name]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_name_display()} - {self.url}"

    @property
    def display_name(self):
        """Returns the human-readable name of the social media platform"""
        return self.get_name_display()

    @property
    def icon_html(self):
        """Returns HTML for the Bootstrap icon"""
        return f'<i class="{self.icon}"></i>' if self.icon else ""


class PhoneNumber(models.Model):
    """
    Stores phone numbers with metadata such as primary use, WhatsApp usage,
    display status, and order.
    """

    class Meta:
        ordering = ["order", "number"]

    number = PhoneNumberField(
        region="KE",
        help_text="Phone number (e.g., +254712345678 or 0712345678)",
        unique=True,
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this phone number should be displayed",
    )
    is_primary = models.BooleanField(
        default=False,
        help_text="Mark as primary phone number. If is_active is False, this will be ignored.",
    )
    use_for_whatsapp = models.BooleanField(
        default=False,
        help_text="Whether this phone number should be used for WhatsApp. If is_active is False, this will be ignored.",
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Enforces business rules:
        - Only one primary number allowed
        - Only one WhatsApp number allowed
        - If inactive, disables primary and WhatsApp flags
        """
        if not self.is_active:
            self.is_primary = False
            self.use_for_whatsapp = False

        if self.is_primary:
            PhoneNumber.objects.filter(is_primary=True).exclude(pk=self.pk).update(
                is_primary=False
            )

        if self.use_for_whatsapp:
            PhoneNumber.objects.filter(use_for_whatsapp=True).exclude(
                pk=self.pk
            ).update(use_for_whatsapp=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.international_format

    @property
    def formatted_number(self):
        """Returns the formatted phone number"""
        return str(self.number)

    @property
    def national_format(self):
        """Returns phone number in national format"""
        return self.number.as_national if self.number else ""

    @property
    def international_format(self):
        """Returns phone number in international format"""
        return self.number.as_international if self.number else ""

    @property
    def tel_link(self):
        """Returns a tel: link for the phone number"""
        return f"tel:{self.number}"

    @property
    def whatsapp_link(self):
        """Returns a WhatsApp link for the phone number"""
        if self.use_for_whatsapp and self.number:
            clean_number = str(self.number).replace("+", "").replace(" ", "")
            return f"https://wa.me/{clean_number}"
        return ""


class EmailAddress(models.Model):
    """
    Stores email addresses with metadata for display, priority,
    and ordering.
    """

    class Meta:
        ordering = ["order", "email"]
        verbose_name_plural = "Email addresses"

    email = models.EmailField(
        help_text="Email address (e.g., user@example.com)",
        unique=True,
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this email address should be displayed",
    )
    is_primary = models.BooleanField(
        default=False,
        help_text="Mark as primary email address. If is_active is False, this will be ignored.",
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Ensures only one email is set as primary and disables primary
        if email is not active.
        """
        if not self.is_active:
            self.is_primary = False

        if self.is_primary:
            EmailAddress.objects.filter(is_primary=True).exclude(pk=self.pk).update(
                is_primary=False
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    @property
    def mailto_link(self):
        """Returns a mailto: link for the email address"""
        return f"mailto:{self.email}"


class PhysicalAddress(models.Model):
    """
    Stores physical addresses, with optional Google Maps embed URLs,
    display order, and contact form preferences.
    """

    class Meta:
        ordering = ["order", "label", "city"]
        verbose_name_plural = "Physical addresses"

    label = models.CharField(
        max_length=100,
        help_text="Custom label for this address e.g Main Office Address",
        unique=True,
    )
    building = models.CharField(
        max_length=100,
        blank=True,
        help_text="Building name or number (e.g., Britam Tower, Block A)",
    )
    street_address = models.CharField(
        max_length=255,
        help_text="Street address including house number and street name",
        blank=True,
    )
    city = models.CharField(max_length=100, help_text="City name", blank=True)
    state_province = models.CharField(
        max_length=100,
        blank=True,
        help_text="State, province, or county (e.g., Vihiga County)",
    )
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        help_text="ZIP code, postal code, or equivalent",
    )
    country = models.CharField(
        max_length=100, default="Kenya", help_text="Country name", blank=True
    )
    map_embed_url = models.URLField(
        blank=True,
        max_length=500,
        help_text="Google Maps/Other map provider embed URL for displaying in iframes",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this address should be displayed",
    )
    use_in_contact_form = models.BooleanField(
        default=False,
        help_text="Mark this as the address to use in contact forms and maps. Only one active address can be selected.",
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Ensures only one address is marked for contact form use.
        Automatically disables this flag if the address is inactive.
        """
        if not self.is_active:
            self.use_in_contact_form = False

        if self.use_in_contact_form:
            PhysicalAddress.objects.filter(use_in_contact_form=True).exclude(
                pk=self.pk
            ).update(use_in_contact_form=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.label if self.label else self.city

    @property
    def full_address(self):
        """Returns the full formatted address string"""
        parts = [self.street_address, self.city]
        if self.state_province:
            parts.append(self.state_province)
        if self.postal_code:
            parts.append(self.postal_code)
        parts.append(self.country)
        return ", ".join(parts)

    @property
    def short_address(self):
        """Returns a shorter city + country format"""
        return f"{self.city}, {self.country}"

    @property
    def google_maps_url(self):
        """Generates a Google Maps search URL for the full address"""
        import urllib.parse

        query = urllib.parse.quote_plus(self.full_address)
        return f"https://www.google.com/maps/search/?api=1&query={query}"


class UserRole(Group):
    """UserGroup with configurable role settings and permissions via admin panel"""

    # Add fields for role configuration
    display_name = models.CharField(
        max_length=100, blank=True, help_text="Human-readable name for this role"
    )
    is_staff_role = models.BooleanField(
        default=False, help_text="Users with this role can log into this admin site."
    )
    is_default_role = models.BooleanField(
        default=False, help_text="New users will be assigned this role by default"
    )
    description = models.TextField(
        blank=True, help_text="Description of this role's purpose and permissions"
    )

    # Permissions are inherited from Django's Group model via the 'permissions' field
    # We can add helper methods to work with them

    def __str__(self):
        return self.get_display_name()

    def get_display_name(self):
        """Get the display name for this role"""
        return self.display_name or self.name.title()

    def clean(self):
        super().clean()
        # Ensure only one default role exists
        if self.is_default_role:
            existing_default = UserRole.objects.filter(is_default_role=True).exclude(
                pk=self.pk
            )

            if existing_default.exists():
                raise ValidationError(
                    "Only one role can be set as the default role. "
                    f"'{existing_default.first().name}' is currently the default."
                )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

        # Update staff status for users with this role after saving
        self._update_users_staff_status()

    def _update_users_staff_status(self):
        """Update staff status for all users with this role"""
        from django.contrib.auth import get_user_model

        User = get_user_model()

        try:
            users_with_role = User.objects.filter(
                groups=self,
                is_superuser=False,  # Skip superusers
            )

            updated_count = 0
            for user in users_with_role:
                if user.is_staff != self.is_staff_role:
                    user.is_staff = self.is_staff_role
                    user.save(update_fields=["is_staff"])
                    updated_count += 1

            if updated_count > 0:
                logger.info(
                    f"Updated staff status for {updated_count} users in role '{self.name}'"
                )

        except Exception as e:
            logger.error(f"Failed to update staff status for role '{self.name}': {e}")

    # Permission-related methods
    def add_permission(self, permission):
        """Add a permission to this role"""
        if isinstance(permission, str):
            # If permission is a string like 'app_label.permission_codename'
            try:
                app_label, codename = permission.split(".")
                permission_obj = Permission.objects.get(
                    content_type__app_label=app_label, codename=codename
                )
                self.permissions.add(permission_obj)
            except (ValueError, Permission.DoesNotExist) as e:
                logger.error(
                    f"Failed to add permission '{permission}' to role '{self.name}': {e}"
                )
        else:
            # If permission is a Permission object
            self.permissions.add(permission)

    def remove_permission(self, permission):
        """Remove a permission from this role"""
        if isinstance(permission, str):
            try:
                app_label, codename = permission.split(".")
                permission_obj = Permission.objects.get(
                    content_type__app_label=app_label, codename=codename
                )
                self.permissions.remove(permission_obj)
            except (ValueError, Permission.DoesNotExist) as e:
                logger.error(
                    f"Failed to remove permission '{permission}' from role '{self.name}': {e}"
                )
        else:
            self.permissions.remove(permission)

    def has_permission(self, permission):
        """Check if this role has a specific permission"""
        if isinstance(permission, str):
            try:
                app_label, codename = permission.split(".")
                return self.permissions.filter(
                    content_type__app_label=app_label, codename=codename
                ).exists()
            except ValueError:
                return False
        else:
            return self.permissions.filter(pk=permission.pk).exists()

    def get_permissions_list(self):
        """Get a list of permission codenames for this role"""
        return list(self.permissions.values_list("content_type__app_label", "codename"))

    def get_permissions_display(self):
        """Get a human-readable list of permissions"""
        permissions = self.permissions.select_related("content_type").all()
        return [
            f"{perm.content_type.app_label}.{perm.codename} ({perm.name})"
            for perm in permissions
        ]

    def set_permissions(self, permission_list):
        """Set permissions for this role (replaces existing permissions)"""
        self.permissions.clear()

        for perm in permission_list:
            if isinstance(perm, str):
                self.add_permission(perm)
            else:
                self.permissions.add(perm)

    @classmethod
    def get_default_role(cls):
        """Get the default role for new users"""
        try:
            return cls.objects.filter(is_default_role=True).first()
        except Exception as e:
            logger.error(f"Error getting default role: {e}")
            return None

    @classmethod
    def get_staff_roles(cls):
        """Get all roles that should have staff status"""
        try:
            return cls.objects.filter(is_staff_role=True)
        except Exception as e:
            logger.error(f"Error getting staff roles: {e}")
            return cls.objects.none()

    @classmethod
    def get_role_staff_status(cls, role_name):
        """Get staff status for a specific role name"""
        try:
            role = cls.objects.get(name=role_name)
            return role.is_staff_role
        except cls.DoesNotExist:
            logger.warning(f"Role '{role_name}' does not exist")
            return False
        except Exception as e:
            logger.error(f"Error getting staff status for role '{role_name}': {e}")
            return False

    @classmethod
    def get_roles_display(cls):
        """Get roles with display names for forms/UI"""
        try:
            return [(role.name, role.get_display_name()) for role in cls.objects.all()]
        except Exception as e:
            logger.error(f"Error getting roles display: {e}")
            return []


class User(AbstractUser):
    """User model with simplified role management and permission checking"""

    def __str__(self):
        return self.username

    def get_role(self):
        """Get the user's role from groups"""
        try:
            role_group = (
                self.groups.select_related().filter(usergroup__isnull=False).first()
            )
            return role_group.name if role_group else "No role assigned"
        except Exception as e:
            logger.error(f"Error getting role for user {self.username}: {e}")
            return "No role assigned"

    def get_role_object(self):
        """Get the UserGroup object for this user's role"""
        try:
            group = self.groups.select_related().filter(usergroup__isnull=False).first()
            if group:
                return UserRole.objects.get(pk=group.pk)
            return None
        except Exception as e:
            logger.error(f"Error getting role object for user {self.username}: {e}")
            return None

    def has_role(self, role_name):
        """Check if user has a specific role"""
        try:
            return self.groups.filter(name=role_name, usergroup__isnull=False).exists()
        except Exception as e:
            logger.error(f"Error checking role for user {self.username}: {e}")
            return False

    def set_role(self, role_name):
        """Set user's role, ensuring only one role group"""
        try:
            # Get the role group
            new_role = UserRole.objects.get(name=role_name)

            # Remove from all existing UserGroup instances
            existing_user_groups = UserRole.objects.filter(user=self)
            self.groups.remove(*existing_user_groups)

            # Add to new role group
            self.groups.add(new_role)

            # Update staff status (but not for superusers)
            if not self.is_superuser:
                old_staff_status = self.is_staff
                self.is_staff = new_role.is_staff_role
                if old_staff_status != self.is_staff:
                    self.save(update_fields=["is_staff"])
                    logger.info(
                        f"Updated staff status for user {self.username} to {self.is_staff}"
                    )

        except UserRole.DoesNotExist:
            raise ValueError(f"Role '{role_name}' does not exist")
        except Exception as e:
            logger.error(f"Error setting role for user {self.username}: {e}")
            raise

    def get_role_permissions(self):
        """Get all permissions from the user's role"""
        role_obj = self.get_role_object()
        if role_obj:
            return role_obj.permissions.all()
        return Permission.objects.none()

    def has_role_permission(self, permission):
        """Check if user has permission through their role"""
        role_obj = self.get_role_object()
        if role_obj:
            return role_obj.has_permission(permission)
        return False

    def get_all_permissions_display(self):
        """Get all permissions (user + role) for display"""
        user_perms = set(self.user_permissions.values_list("id", flat=True))
        role_perms = set()

        role_obj = self.get_role_object()
        if role_obj:
            role_perms = set(role_obj.permissions.values_list("id", flat=True))

        all_perm_ids = user_perms | role_perms
        permissions = Permission.objects.filter(id__in=all_perm_ids).select_related(
            "content_type"
        )

        return [
            {
                "permission": f"{perm.content_type.app_label}.{perm.codename}",
                "name": perm.name,
                "source": "role" if perm.id in role_perms else "user",
            }
            for perm in permissions
        ]

    def clean(self):
        """Validate that user has at most one role"""
        super().clean()

        if self.pk:  # Only validate for existing users
            try:
                user_roles = self.groups.filter(usergroup__isnull=False)
                if user_roles.count() > 1:
                    role_names = [role.name for role in user_roles]
                    raise ValidationError(
                        f"User can only belong to one role group. "
                        f"Currently assigned to: {', '.join(role_names)}"
                    )
            except Exception as e:
                logger.error(f"Error validating user roles for {self.username}: {e}")

    @property
    def role(self):
        """Property to get role"""
        return self.get_role()

    def save(self, *args, **kwargs):
        """Override save to assign default role, handle superusers, and update staff status"""
        is_new = self.pk is None
        old_staff_status = None if is_new else self.is_staff

        # Ensure superusers are always staff
        if self.is_superuser and not self.is_staff:
            self.is_staff = True

        # Validate before saving
        if not is_new:
            self.clean()

        # Save first to ensure we have a pk for M2M operations
        super().save(*args, **kwargs)

        # For new users, assign default role first
        if is_new:
            self._assign_default_role()

        # Update staff status based on current group membership (for both new and existing users)
        if not self.is_superuser:  # Don't modify superuser staff status
            self._update_staff_status_from_groups()

        # Log staff status changes for existing users
        if (
            not is_new
            and old_staff_status is not None
            and old_staff_status != self.is_staff
        ):
            logger.info(
                f"Updated staff status for user {self.username} from {old_staff_status} to {self.is_staff}"
            )

    def _update_staff_status_from_groups(self):
        """Update staff status based on current group membership"""
        try:
            # Get the user's role group
            role_obj = self.get_role_object()

            if role_obj:
                # Update staff status based on role
                new_staff_status = role_obj.is_staff_role

                if self.is_staff != new_staff_status:
                    self.is_staff = new_staff_status
                    # Use update_fields to avoid recursion
                    User.objects.filter(pk=self.pk).update(is_staff=new_staff_status)
                    logger.info(
                        f"Updated staff status for user {self.username} to {new_staff_status} based on role '{role_obj.name}'"
                    )
            else:
                # No role assigned, remove staff status unless they're a superuser
                if self.is_staff and not self.is_superuser:
                    self.is_staff = False
                    User.objects.filter(pk=self.pk).update(is_staff=False)
                    logger.info(
                        f"Removed staff status for user {self.username} (no role assigned)"
                    )

        except Exception as e:
            logger.error(f"Error updating staff status for user {self.username}: {e}")

    def _assign_default_role(self):
        """Assign default role to new user"""
        try:
            if not self.groups.filter(usergroup__isnull=False).exists():
                default_role = UserRole.get_default_role()
                if default_role:
                    self.set_role(default_role.name)
                    logger.info(
                        f"Assigned default role '{default_role.name}' to new user {self.username}"
                    )
                else:
                    logger.warning(
                        f"No default role found for new user {self.username}"
                    )
        except Exception as e:
            logger.error(f"Failed to assign default role to user {self.username}: {e}")
