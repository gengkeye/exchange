# -*- coding: utf-8 -*-
#
from __future__ import unicode_literals

from django.db  import models
from django.db.models import Avg, Sum, Count, Value, Q
from django.db.models.functions import Concat

import datetime
from decimal import Decimal
from django.conf import settings

from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

@python_2_unicode_compatible
class TeleUser(models.Model):
    ROLE_CHOICES = (
        ('Admin', 'Administrator'),
        ('GroupAdmin', 'Group Administrator'),
        ('Driver', 'Driver'),
        ('Merchant', 'Merchant'),
        ('User', 'Common User'),
    )
    CREDIT_LEVEL_CHOICES = (
        ('A', 'A'),
        ('AA', 'AA'),
        ('AAA', 'AAA'),
    )
    chat_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    username = models.CharField(max_length=20, unique=True, blank=True, null=True)
    short_name = models.CharField(max_length=10, unique=True, blank=True, null=True)
    role = models.CharField(choices=ROLE_CHOICES, default='User', max_length=20, blank=True)
    credit_level = models.CharField(choices=CREDIT_LEVEL_CHOICES, default='A', max_length=20, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def is_admin(self):
        return self.role in ['Admin', 'GroupAdmin']

    @property
    def is_superuser(self):
        return self.role == 'Admin'
            
    def is_member_of(self, group):
        if self.is_superuser or self.membership.filter(group=group):
            return True
        else:
            return False

@python_2_unicode_compatible
class TeleImage(models.Model):
    PURPOSE_CHOICES = (
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Supper', 'Supper'),
        ('others', 'others')
    )
    image_id = models.CharField(max_length=100, unique=True)
    from_user = models.ForeignKey(TeleUser, on_delete=models.SET_NULL, blank=True, null=True)
    purpose = models.CharField(choices=PURPOSE_CHOICES, max_length=20, default='Breakfast')

    def __str__(self):
        return self.image_id


@python_2_unicode_compatible
class TeleGroup(models.Model):
    title = models.CharField(max_length=20, unique=True, blank=True, null=True)
    chat_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    driver = models.ForeignKey(TeleUser, on_delete=models.SET_NULL, related_name='drived_group', blank=True, null=True)
    managers = models.ManyToManyField(TeleUser, related_name='managed_groups', blank=True)
    members = models.ManyToManyField(TeleUser, through='TeleMembership')
    images = models.ManyToManyField(TeleImage)
    address = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    remarks = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.chat_id

    @property
    def last_order(self):
        return self.orders.get(status='open')


@python_2_unicode_compatible
class TeleMembership(models.Model):
    user = models.ForeignKey(TeleUser, on_delete=models.CASCADE, related_name='membership')
    group = models.ForeignKey(TeleGroup, on_delete=models.CASCADE, related_name='membership')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    subscribed = models.BooleanField(default=False)

    def __str__(self):
        return "%s %s: %s"%(self.user.name, self.group.title, str(self.balance))

@python_2_unicode_compatible
class Bid(models.Model):
    CURRENCY_CHOICES = (
        ('CNY', _("CNY")),
        ('PHP', _("PHP")),
        ('USD', _("USD")),
        # ('TWD', _("TWD")),
        # ('MYR', _("MYR")),
        # ('SGD', _("SGD")),
        # ('JPY', _("JPY")),
        # ('KRW', _("KRW")),
        # ('EUR', _("EUR")),
        # ('HKD', _("HKD")),
        # ('INR', _("INR")),
        # ('THB', _("THB")),
        # ('AUD', _("AUD")),
    )

    user = models.ForeignKey(TeleUser, on_delete=models.CASCADE, related_name='bids')
    sell_currency = models.CharField(choices=CURRENCY_CHOICES, max_length=30)
    buy_currency = models.CharField(choices=CURRENCY_CHOICES, max_length=30)
    max_amount = models.PositiveIntegerField(default=0)
    min_amount = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    date_created = models.DateTimeField(auto_now_add=True)


