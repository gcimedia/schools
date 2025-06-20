# Generated migration file


from django.core.management import call_command
from django.db import migrations

from ..models import BASE_DETAIL_CHOICES, BASE_IMAGE_CHOICES


def setup_npm_packages(apps, schema_editor):
    """
    Setup npm packages by uninstalling all and then installing defaults.
    """
    # First, uninstall all existing packages
    call_command("npm", "uninstall", "--all", verbosity=1)

    # Then, install the default packages
    call_command("npm", "install", verbosity=1)


def create_choice_instances(apps, schema_editor):
    """
    Forward migration: Create instances for all choices in BaseDetail and BaseImage.
    """
    BaseDetail = apps.get_model("core", "BaseDetail")
    BaseImage = apps.get_model("core", "BaseImage")

    # Create ORDER_MAPPING for BaseDetail
    base_detail_order_mapping = {
        key: i + 1 for i, (key, _) in enumerate(BASE_DETAIL_CHOICES)
    }

    # Create BaseDetail instances for all choices
    for choice_key, choice_display in BASE_DETAIL_CHOICES:
        BaseDetail.objects.get_or_create(
            name=choice_key,
            defaults={
                "value": "",  # Empty value as requested
                "ordering": base_detail_order_mapping.get(choice_key, 999),
            },
        )

    # Create ORDER_MAPPING for BaseImage
    base_image_order_mapping = {
        key: i + 1 for i, (key, _) in enumerate(BASE_IMAGE_CHOICES)
    }

    # Create BaseImage instances for all choices
    for choice_key, choice_display in BASE_IMAGE_CHOICES:
        BaseImage.objects.get_or_create(
            name=choice_key,
            defaults={
                "image": None,  # Empty image field
                "ordering": base_image_order_mapping.get(choice_key, 999),
            },
        )


def forward_migration(apps, schema_editor):
    """
    Combined forward migration: Setup npm packages and create choice instances.
    """
    # First, setup npm packages
    setup_npm_packages(apps, schema_editor)
    # Then, create choice instances
    create_choice_instances(apps, schema_editor)


def reverse_choice_instances(apps, schema_editor):
    """
    Reverse migration: Remove all instances created by this migration.
    """
    BaseDetail = apps.get_model("core", "BaseDetail")
    BaseImage = apps.get_model("core", "BaseImage")

    # Delete only the specific choice instances, not all instances
    choice_keys_detail = [key for key, _ in BASE_DETAIL_CHOICES]
    BaseDetail.objects.filter(name__in=choice_keys_detail).delete()

    choice_keys_image = [key for key, _ in BASE_IMAGE_CHOICES]
    BaseImage.objects.filter(name__in=choice_keys_image).delete()


def cleanup_npm_packages(apps, schema_editor):
    """
    Reverse npm setup by removing all packages.
    """
    call_command("npm", "uninstall", "--all", verbosity=1)


def reverse_migration(apps, schema_editor):
    """
    Combined reverse migration: Remove choice instances and cleanup npm packages.
    """
    # First, remove choice instances
    reverse_choice_instances(apps, schema_editor)
    # Then, cleanup npm packages
    cleanup_npm_packages(apps, schema_editor)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            forward_migration,
            reverse_migration,
        ),
    ]
