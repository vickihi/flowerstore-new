import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flowerstore.settings")
django.setup()

from accounts.models import Account

email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
full_name = os.environ.get("DJANGO_SUPERUSER_FULL_NAME", "Admin")

if email and password and not Account.objects.filter(email=email).exists():
    Account.objects.create_superuser(email=email, full_name=full_name, password=password)
    print(f"Superuser {email} created.")
else:
    print("Superuser already exists or env vars missing.")
