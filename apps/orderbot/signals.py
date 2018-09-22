from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _

from django.conf import settings
from .models import TeleOrder, TeleUser, TeleMembership, TeleBalanceHistory

@receiver(pre_save, sender = TeleOrder)
def order_status_changed(sender, instance, **kwargs):
	if instance.id and instance.status == 'closed':
		for i in instance.items.values_list('user_id', flat=True).distinct():
			u = TeleUser.objects.get(id=i)
			u.change_balance(settings.FEE, instance.group, 'minus', 'fee', 'System')


@receiver(pre_save, sender = TeleMembership)
def balance_changed(sender, instance, **kwargs):
	if instance.id:
		old_instance = TeleMembership.objects.get(id=instance.id)
		if instance.balance != old_instance.balance:
			TeleBalanceHistory.objects.create(
				user=instance.user,
				group=instance.group,
				before=old_instance.balance,
				after=instance.balance,
				diff=instance.balance - old_instance.balance,
				category=getattr(instance, '_categroy', 'fee'),
				created_by=getattr(instance, '_created_by', 'System'),
			)


