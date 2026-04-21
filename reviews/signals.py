from django.db.models.signals import post_save
from django.dispatch import receiver

from reviews.models.flag import Flag


@receiver(post_save, sender=Flag)
def on_flag_saved(sender, instance, **kwargs):
    instance.review.update_hidden_status()
