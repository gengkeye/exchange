from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import ThumbsUp
from .utils import get_object_or_none


@receiver(pre_save, sender=ThumbsUp)
def after_create_thumb_up(sender, instance, **kwargs):
    old_instance = get_object_or_none(ThumbsUp, pk=instance.pk)
    store = instance.store
    if old_instance and old_instance.like != instance.like:
        if instance.like:
            store.likes += 1
            store.dislikes -= 1
        else:
            store.dislikes += 1
            store.likes -= 1
    else:
        if instance.like:
            store.likes += 1
        else:
            store.dislikes += 1

    store.save()


