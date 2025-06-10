import logging

from django.db.models.signals import post_migrate
from django.dispatch import receiver

from apps.home.config.auth import auth_config

logger = logging.getLogger(__name__)


@receiver(post_migrate)
def setup_school_roles(sender, **kwargs):
    """
    Setup roles and groups after migrations.
    """
    try:
        # Create the groups if they don't exist
        auth_config.create_groups_if_needed()

        # Update staff status for all existing users based on their roles
        auth_config.bulk_update_staff_status()

    except Exception as e:
        logger.warning(f"Failed to create school groups or update staff status: {e}")
