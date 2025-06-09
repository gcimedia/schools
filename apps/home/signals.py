from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .admin_site import org_admin_site
from .models import OrgDetail


def set_admin_site_titles():
    """
    Sets the Django admin site's title, header, and index title
    based on the 'org_name' value stored in the OrgDetail model.
    If the value is not found, default titles are used.
    """
    org_name = OrgDetail.objects.filter(name="org_name").first()
    org_admin_site.site_title = (
        org_name.value if org_name else "Organisation site admin"
    )
    org_admin_site.site_header = (
        org_name.value if org_name else "Organisation Administration"
    )
    org_admin_site.index_title = "Site administration"


@receiver(post_save, sender=OrgDetail)
@receiver(post_delete, sender=OrgDetail)
def update_admin_site_titles(sender, **kwargs):
    """
    Signal receiver that updates the admin site titles whenever an OrgDetail
    instance is saved or deleted.

    This ensures the admin reflects the latest organization name if updated.
    """
    set_admin_site_titles()
