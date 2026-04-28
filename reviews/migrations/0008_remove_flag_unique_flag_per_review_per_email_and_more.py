from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0002_add_category_image"),
        ("reviews", "0007_alter_vote_unique_together"),
    ]

    operations = []