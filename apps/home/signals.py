import logging

from django.core.cache import cache  # Import cache
from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver

from apps.home.config.auth import auth_config

from .admin_site import admin_site
from .models import BaseDetail, BaseImage, User  # Import BaseImage

logger = logging.getLogger(__name__)


@receiver(post_save, sender=BaseDetail)
@receiver(post_delete, sender=BaseDetail)
def update_admin_site_titles(sender, **kwargs):
    """
    Signal receiver that updates the admin site titles whenever an OrgDetail
    instance is saved or deleted.

    This ensures the admin reflects the latest organization name if updated.
    """
    base_name = BaseDetail.objects.filter(name="base_name").first()
    admin_site.site_title = base_name.value if base_name else "Organisation site admin"
    admin_site.site_header = (
        f"{base_name.value} Admin" if base_name else "Organisation Administration"
    )


@receiver(post_save, sender=BaseDetail)
@receiver(post_delete, sender=BaseDetail)
@receiver(post_save, sender=BaseImage)
@receiver(post_delete, sender=BaseImage)
def clear_base_config_cache(sender, **kwargs):
    """
    Signal receiver to clear the 'base_config' cache whenever BaseDetail
    or BaseImage instances are saved or deleted, ensuring fresh data.
    """
    # logger.info(f"Clearing 'base_config' cache due to {sender.__name__} change.")
    cache.delete("base_config")


@receiver(m2m_changed, sender=User.groups.through)
def update_user_staff_status_on_group_change(
    sender, instance, action, pk_set, **kwargs
):
    """
    Update user's staff status when their groups change via admin or any other method.
    This ensures staff status stays in sync with role-based groups.
    """
    if action in ("post_add", "post_remove", "post_clear"):
        try:
            # Don't modify superuser staff status
            if not instance.is_superuser:
                # Get the user's current role and update staff status accordingly
                current_role = instance.get_role()
                if current_role and current_role != "No role assigned":
                    should_be_staff = auth_config.get_role_staff_status(current_role)
                    if instance.is_staff != should_be_staff:
                        instance.is_staff = should_be_staff
                        instance.save(update_fields=["is_staff"])
                        logger.info(
                            f"Updated staff status for user {instance.username} to {should_be_staff} based on role {current_role}"
                        )
        except Exception as e:
            logger.warning(
                f"Failed to update staff status for user {instance.username}: {e}"
            )
