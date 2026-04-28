from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0002_add_category_image"),
        ("orders", "0001_initial"),
    ]

    operations = []