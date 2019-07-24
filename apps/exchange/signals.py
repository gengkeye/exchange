from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ThumbsUp


@receiver(post_save, sender=ThumbsUp)
def after_create_thumb_up(sender, instance, created, **kwargs):
    if created:
        store = instance.store
        if instance.like:
            store.likes += 1
        else:
            store.dislikes += 1
        store.save() 

