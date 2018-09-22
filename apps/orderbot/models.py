# -*- coding: utf-8 -*-
#
from __future__ import unicode_literals

from django.db  import models
from django.db.models import Avg, Sum, Count, Value, Q
from django.db.models.functions import Concat

import datetime
from decimal import Decimal

from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django_mysql.models import GroupConcat

from django.conf import settings

__all__ = ['TeleUser', 'TeleGroup', 'TeleMembership', 'TeleImage']


@python_2_unicode_compatible
class TeleUser(models.Model):
    ROLE_CHOICES = (
        ('Admin', 'Administrator'),
        ('GroupAdmin', 'Group Administrator'),
        ('Driver', 'Driver'),
        ('Merchant', 'Merchant'),
        ('User', 'Common User'),
    )
    chat_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    username = models.CharField(max_length=20, unique=True, blank=True, null=True)
    role = models.CharField(choices=ROLE_CHOICES, default='User', max_length=20, blank=True)
    enabled_notice = models.BooleanField(default=False)
    last_notice_at = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    last_get_money_at = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    time_interval_days = models.PositiveSmallIntegerField(default=1)


    def __str__(self):
        return self.name

    @property
    def url(self):
        if self.username:
            return "https://t.me/%s" % self.username
            # return "@%s" % self.username

        else:
            return None

    @property
    def is_admin(self):
        return self.role in ['Admin', 'GroupAdmin']

    @property
    def is_superuser(self):
        return self.role == 'Admin'

    @property
    def can_notice(self):
        if self.is_superuser:
            return True
        if not self.enabled_notice:
            return False
        if not self.last_notice_at:
            return True
        if not self.last_notice_at or \
            self.last_notice_at.date() + datetime.timedelta(days=self.time_interval_days) <= datetime.datetime.today().date():
            return True
        return False

    @property
    def cat_get_money(self):
        if (not self.last_get_money_at) or \
            (self.last_get_money_at.date() + datetime.timedelta(days=self.time_interval_days) <= datetime.datetime.today().date()):
            return True
        return False
            
    def is_member_of(self, group):
        if self.is_superuser or self.membership.filter(group=group):
            return True
        else:
            return False

    def change_balance(self, amount, group, operator, category, created_by):
        membership, r = TeleMembership.objects.get_or_create(group=group, user=self)
        before_balance = membership.balance
        if operator == 'add':   
            membership.balance = Decimal(before_balance) + amount
        elif operator == 'minus':
            membership.balance = Decimal(before_balance) - amount
        membership._category = category
        membership._created_by = created_by
        membership.save()


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
class TeleStore(models.Model):
    LEVEL_CHOICES = (
        ('Five', 'Five Stars'),
        ('Four', 'Four Stars'),
        ('Three', 'Three Stars'),
        ('Two', 'Two Stars'),
        ('One', 'One Star')
    )
    name = models.CharField(max_length=20, unique=True)
    owner = models.ForeignKey(TeleUser, on_delete=models.SET_NULL, blank=True, null=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    wechat_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    active = models.BooleanField(default= False)
    level = models.CharField(choices=LEVEL_CHOICES, max_length=20, default='Three', blank=True)
    supply_bre = models.BooleanField(default=False)
    supply_lun = models.BooleanField(default=False)
    supply_sup = models.BooleanField(default=False)
    remarks = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    @property
    def siblings(self):
        return TeleStore.objects.exclude(id=self.id)

    @classmethod
    def available(cls):
        return cls.objects.filter(active=True)


@python_2_unicode_compatible
class TeleProduct(models.Model):
    PURPOSE_CHOICES = (
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Supper', 'Supper'),
        ('All', 'All'),
    )
    Day_CHOICES = (
        ('0', 'Anyday'),
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
        ('7', 'Sunday'),
    )
    CATEGORY_CHOICES = (
        ('0', 'vegetables'),
        ('1', 'meat'),
        ('2', 'littemeat'),
        ('3', 'fruit'),
        ('4', 'rice'),
        ('5', 'soup'),
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_union_price = models.BooleanField(default=False)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10, default='0')
    store = models.ForeignKey(TeleStore, on_delete=models.CASCADE, related_name='products')
    role = models.CharField(choices=PURPOSE_CHOICES, max_length=20, default='Breakfast')
    enabled_day = models.CharField(choices=Day_CHOICES, max_length=10, default='0')

    def __str__(self):
        return self.name

    @classmethod
    def enabled(cls):
        return cls.objects.filter(
            store__active=True,
            enabled_day__in=[0, datetime.datetime.today().weekday()+1],
        )


@python_2_unicode_compatible
class TelePricePolicy(models.Model):
    unioncode = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    store = models.ForeignKey(TeleStore, on_delete=models.CASCADE, related_name='price_policies')

    def __str__(self):
        return "%s %s: %s"%(self.store.name, self.unioncode, str(self.price))


@python_2_unicode_compatible
class TeleOrder(models.Model):
    STATUS_CHOICES=(
        ('open', 'epen'),
        ('closed', 'closed'),
        ('shipped', 'shipped'),
        ('received', 'received'),
        ('invalid', 'invalid'),
    )
    date_created = models.DateTimeField(auto_now_add=True)
    delivery_at = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    status = models.CharField(choices=STATUS_CHOICES, default='open', max_length=10)
    group = models.ForeignKey(TeleGroup, on_delete=models.CASCADE, related_name='orders', default=1)
    store = models.ForeignKey(TeleStore, on_delete=models.SET_NULL, null=True, related_name='orders', default=1)

    def __str__(self):
        return self.group.name

    def summary(self):
        message = ''
        if self.items.first().code:
            # for lunch with code
            items = self.items.values('code')
            for  item in items:
                message += item['code'] + '\n'
        else:
            # for breakfast without code
            items = self.items.values('product_id', 'product__name').annotate(
                total_amount = Sum('amount'),
            )
            for  item in items:
                message += item['product__name'] + '*' + str(item['total_amount']) + '\n'

        group = self.group
        message += _("Address: %(address)s, Phone: %(phone)s, Remark: %(remark)s, Total: %(total)s") \
            % {'address': group.address, 
                'phone': group.phone, 
                'remark': group.remarks, 
                'total': str(self.items.aggregate(Sum('total'))['total__sum']) }
        return message


    def show_order(self):
        items = self.items.values('user__name', 'is_union_price').annotate(
            description=GroupConcat('description', separator=', '),
            total_price=Sum('total'),
            code=GroupConcat('code', separator=' '),
        )
        message = _("Order ID: %(orderid)s, Date: %(orderdate)s, Order detail:") \
            % {'orderid': self.id, 'orderdate': self.date_created } + '\n' \
            + '---------------' + '\n'
        for item in items:
            message += item['user__name'] + ': ' + item['code'] \
                + ' ' + item['description'] + ' ' + str(item['total_price']) + ' '+ '\n'
        group = self.group
        message += _("Address: %(address)s, Phone: %(phone)s, Remark: %(remark)s, Total: %(total)s") \
            % {'address': group.address, 
                'phone': group.phone, 
                'remark': group.remarks, 
                'total': str(self.items.aggregate(Sum('total'))['total__sum']) }
        return message

    def close(self):
        self.status = 'closed'
        self.save()

    def discard(self):
        items = self.items.values('user_id').annotate(total_price=Sum('total'))
        for item in items:
            item_user =  TeleUser.objects.get(id=item['user_id'])
            try:
                item_user.change_balance(Decimal(item['total_price'] + settings.FEE), self.group, 'add', 'discard_order', 'Admin')
            except:
                return _('cannot_be_discarded')
        self.status = 'invalid'
        self.save()
        return _('discard_order_success')


@python_2_unicode_compatible
class  TeleOrderItem(models.Model):
    order = models.ForeignKey(TeleOrder, on_delete=models.CASCADE, related_name='items')
    user = models.ForeignKey(TeleUser, on_delete=models.CASCADE, related_name='order_items', default=1)
    product = models.ForeignKey(TeleProduct, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.PositiveSmallIntegerField(default=1)
    is_union_price = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=100, blank=True)
    code = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.user.name


@python_2_unicode_compatible
class TeleBalanceHistory(models.Model):
    CATEGORY_CHOICES = (
        ('create_orderitem', 'create order item'),
        ('delete_orderitem', 'delete order item'),
        ('cancel_order', 'cancel order'),
        ('discard_order', 'discard order'),
        ('recharge', 'recharge'),
        ('transfer', 'transfer'),
        ('fee', 'fee'),
    )
    CREATOR_CHOICES = (
        ('Admin',_('Administrator')),
        ('Driver',_('Driver')),
        ('System', _('System')),
    )
    user = models.ForeignKey(TeleUser, on_delete=models.CASCADE, related_name='balance_history')
    order = models.ForeignKey(TeleOrder, on_delete=models.SET_NULL, related_name='balances', blank=True, null=True)
    group = models.ForeignKey(TeleGroup, on_delete=models.SET_NULL, related_name='balance_history', blank=True, null=True)
    before = models.DecimalField(max_digits=10, decimal_places=2)
    after = models.DecimalField(max_digits=10, decimal_places=2)
    diff = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
    remarks = models.CharField(max_length=100, blank=True)
    created_by = models.CharField(choices=CREATOR_CHOICES, max_length=30)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s"%(self.user.name, self.group.name)


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


