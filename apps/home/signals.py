import logging

from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver

from apps.home.config.auth import auth_config

from .admin_site import org_admin_site
from .models import OrgDetail, User

logger = logging.getLogger(__name__)


@receiver(post_save, sender=OrgDetail)
@receiver(post_delete, sender=OrgDetail)
def update_admin_site_titles(sender, **kwargs):
    """
    Signal receiver that updates the admin site titles whenever an OrgDetail
    instance is saved or deleted.

    This ensures the admin reflects the latest organization name if updated.
    """
    org_name = OrgDetail.objects.filter(name="org_name").first()
    org_admin_site.site_title = (
        org_name.value if org_name else "Organisation site admin"
    )
    org_admin_site.site_header = (
        org_name.value if org_name else "Organisation Administration"
    )
    org_admin_site.index_title = "Site administration"


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
