from django.contrib.auth.models import AbstractUser, Group
from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.home.config.auth import auth_config


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


class OrgDetail(UniqueChoiceBaseModel):
    """
    Represents a customizable organization text detail, such as name, motto,
    theme color, or URLs.
    """

    class Meta(UniqueChoiceBaseModel.Meta):
        verbose_name = "App Detail"
        verbose_name_plural = "App Details"

    CHOICES = [
        ("org_name", "Name"),
        ("org_description", "Motto"),
        ("org_theme_color", "Theme Color"),
        ("org_url", "Website URL"),
        ("org_author", "Author's Name"),
        ("org_author_url", "Author's Website URL"),
    ]
    ORDER_MAPPING = {key: i + 1 for i, (key, _) in enumerate(CHOICES)}

    name = models.CharField(max_length=25, choices=CHOICES, unique=True)
    value = models.CharField(
        max_length=255, blank=True, help_text="Value for the organization detail."
    )


class OrgImage(UniqueChoiceBaseModel):
    """
    Represents organization-related image assets like logos, favicons,
    and hero images.
    """

    class Meta(UniqueChoiceBaseModel.Meta):
        verbose_name = "App Image"
        verbose_name_plural = "App Images"

    CHOICES = [
        ("org_logo", "Logo"),
        ("org_favicon", "Favicon"),
        ("org_apple_touch_icon", "Apple Touch Icon"),
        ("org_cover_image", "Cover / Hero image"),
    ]
    ORDER_MAPPING = {key: i + 1 for i, (key, _) in enumerate(CHOICES)}

    name = models.CharField(max_length=25, choices=CHOICES, unique=True)
    image = models.ImageField(
        upload_to="home/org",
        null=True,
        blank=True,
        help_text="Image file for logos, favicons, etc.",
    )


class SocialMedia(models.Model):
    """
    Represents a social media link with associated Bootstrap icon class,
    display status, and display order.
    """

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Social Media"

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
        verbose_name_plural = "Email Addresses"

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
        verbose_name_plural = "Physical Addresses"

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


class User(AbstractUser):
    FALLBACK_ROLES = ["standard", "admin"]

    def __str__(self):
        return self.username

    def get_role(self):
        """Get the user's role from groups"""
        role_groups = auth_config.get_roles()
        if not role_groups:
            role_groups = self.FALLBACK_ROLES

        try:
            user_groups = self.groups.filter(name__in=role_groups).first()
            if user_groups:
                return user_groups.name
        except Exception:
            pass

        return "No role assigned"

    def has_role(self, role_name):
        """Check if user has a specific role"""
        try:
            return self.groups.filter(name=role_name).exists()
        except Exception:
            return False

    def set_role(self, role_name):
        """Set user's role, ensuring only one role group and updating staff status"""
        role_groups = auth_config.get_roles()
        if not role_groups:
            role_groups = self.FALLBACK_ROLES

        if role_name not in role_groups:
            raise ValueError(f"Invalid role: {role_name}. Valid roles: {role_groups}")

        # Remove from all role groups first
        existing_role_groups = Group.objects.filter(name__in=role_groups)
        self.groups.remove(*existing_role_groups)

        # Add to new role group
        group, _ = Group.objects.get_or_create(name=role_name)
        self.groups.add(group)

        # Update staff status based on role (but not for superusers)
        if not self.is_superuser:
            self._update_staff_status_from_role(role_name)

    def _update_staff_status_from_role(self, role_name=None):
        """Update user's staff status based on their role"""
        # Don't modify staff status for superusers - they should always remain staff
        if self.is_superuser:
            return

        if role_name is None:
            role_name = self.get_role()

        if role_name and role_name != "No role assigned":
            should_be_staff = auth_config.get_role_staff_status(role_name)
            if self.is_staff != should_be_staff:
                self.is_staff = should_be_staff
                # Only save if we're not in the middle of a save operation
                if self.pk and hasattr(self, "_state") and not self._state.adding:
                    self.save(update_fields=["is_staff"])

    def _assign_superuser_role(self):
        """Assign appropriate role to superusers"""
        try:
            # Try to assign to admin role if it exists
            staff_roles = auth_config.get_staff_roles()
            if staff_roles:
                # Prefer 'admin' role, or use the first staff role available
                admin_role = "admin" if "admin" in staff_roles else staff_roles[0]
                self.set_role(admin_role)
            elif "admin" in auth_config.get_roles():
                # If admin role exists but isn't marked as staff, still assign it
                self.set_role("admin")
                # And mark admin role as staff for future users
                auth_config.set_role_staff_status("admin", True)
        except Exception:
            # If role assignment fails, that's okay - superuser will still be staff
            pass

    def clean(self):
        """Validate that user has exactly one role"""
        super().clean()

        role_groups = auth_config.get_roles()
        if not role_groups:
            return  # Skip validation if no roles registered yet

        try:
            user_role_groups = self.groups.filter(name__in=role_groups)
            if user_role_groups.count() > 1:
                raise ValidationError("User can only belong to one role group.")
        except Exception:
            # Skip validation if there are database issues
            pass

    @property
    def role(self):
        """Property to get role like the old field"""
        return self.get_role()

    def save(self, *args, **kwargs):
        """Override save to assign default role, update staff status, and handle superusers"""
        self.full_clean()

        is_new = self.pk is None

        # Ensure superusers are always staff
        if self.is_superuser and not self.is_staff:
            self.is_staff = True

        super().save(*args, **kwargs)

        if is_new:
            # Handle role assignment for new users
            if self.is_superuser:
                # For superusers, assign them to admin role if it exists
                self._assign_superuser_role()
            else:
                # Check if user has any role
                role_groups = auth_config.get_roles()
                if role_groups:
                    try:
                        if not self.groups.filter(name__in=role_groups).exists():
                            default_role = auth_config.get_default_role()
                            if default_role:
                                self.set_role(default_role)
                    except Exception:
                        # Skip role assignment if there are issues
                        pass
        else:
            # Update staff status for existing users when they're saved
            # But don't override superuser staff status
            if not self.is_superuser:
                self._update_staff_status_from_role()
