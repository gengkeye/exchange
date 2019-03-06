from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _

from django.conf import settings
from .models import Bid
from .utils import chr_width, get_object_or_none

# @receiver(post_save, sender = Bid)
# def create_short_name(sender, instance, created, **kwargs):
#     if created:
#     	delete_expired_bids()

# @receiver(pre_save, sender = TeleUser)
# def update_short_name(sender, instance, **kwargs):
#     old_instance = get_object_or_none(TeleUser, id=instance.id)
#     if old_instance and instance.name != old_instance.name:
#         set_short_name(instance, instance.name)

# def set_short_name(instance, name):
#     length = 0
#     short_name = ''
#     if name:
#         for n in name:
#             if length < 9:
#                 short_name += n
#             length += chr_width(n)
#         instance.short_name = short_name

