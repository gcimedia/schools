from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .admin_site import org_admin_site
from .models import OrgDetail


def set_admin_site_titles():
    # Fetch OrgDetail values
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
    set_admin_site_titles()
