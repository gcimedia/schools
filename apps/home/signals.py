import logging

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver

from .models import BaseDetail, BaseImage

logger = logging.getLogger(__name__)
User = get_user_model()


@receiver(post_save, sender=BaseDetail)
@receiver(post_delete, sender=BaseDetail)
@receiver(post_save, sender=BaseImage)
@receiver(post_delete, sender=BaseImage)
def clear_base_config_cache(sender, **kwargs):
    """Clear base config cache when BaseDetail or BaseImage changes"""
    try:
        cache.delete("base_config")
        logger.debug(f"Cleared 'base_config' cache due to {sender.__name__} change")
    except Exception as e:
        logger.error(f"Error clearing base config cache: {e}")


@receiver(m2m_changed, sender=User.groups.through)
def update_user_staff_status_on_group_change(
    sender, instance, action, pk_set, **kwargs
):
    """Update user staff status when group membership changes"""

    # Only handle post_add and post_remove actions
    if action not in ["post_add", "post_remove", "post_clear"]:
        return

    try:
        # Skip superusers
        if instance.is_superuser:
            return

        # Get the user's current role
        role_obj = instance.get_role_object()

        if role_obj:
            # Update staff status based on role
            new_staff_status = role_obj.is_staff_role
        else:
            # No role assigned, remove staff status
            new_staff_status = False

        # Update if changed
        if instance.is_staff != new_staff_status:
            # Use update to avoid triggering save() and potential recursion
            User.objects.filter(pk=instance.pk).update(is_staff=new_staff_status)

            action_desc = {
                "post_add": "added to group",
                "post_remove": "removed from group",
                "post_clear": "cleared from all groups",
            }.get(action, action)

            logger.info(
                f"Updated staff status for user {instance.username} to {new_staff_status} "
                f"after being {action_desc}"
            )

    except Exception as e:
        logger.error(
            f"Error updating staff status for user {instance.username} on group change: {e}"
        )
