from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0002_add_category_image"),
        ("orders", "0002_orderitem_unique_order_item"),
    ]

    operations = []