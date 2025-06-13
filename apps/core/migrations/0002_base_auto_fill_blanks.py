# Generated migration file

from django.db import migrations

from ..models import BASE_DETAIL_CHOICES, BASE_IMAGE_CHOICES


def create_choice_instances(apps, schema_editor):
    """
    Forward migration: Create instances for all choices in BaseDetail and BaseImage
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


def reverse_choice_instances(apps, schema_editor):
    """
    Reverse migration: Remove all instances (optional - you might want to keep data)
    """
    BaseDetail = apps.get_model("core", "BaseDetail")
    BaseImage = apps.get_model("core", "BaseImage")

    # Delete only the specific choice instances, not all instances
    choice_keys = [key for key, _ in BASE_DETAIL_CHOICES]
    BaseDetail.objects.filter(name__in=choice_keys).delete()

    choice_keys = [key for key, _ in BASE_IMAGE_CHOICES]
    BaseImage.objects.filter(name__in=choice_keys).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            create_choice_instances,
            reverse_choice_instances,
        ),
    ]
