# ~*~ coding: utf-8 ~*~
#
from __future__ import absolute_import

from celery import shared_task
from celery.signals import celeryd_init
from django.conf import settings
from django.utils.translation import ugettext as _

import telepot
import asyncio
from telepot.aio.loop import MessageLoop
from telepot.aio.delegate import pave_event_space, create_open, per_from_id
from exchange.telepot_utils import MessageHandler
from forex_python.converter import CurrencyRates

from exchange.models import Rate, TeleUser, Bid

TOKEN = settings.TELEGRAM_BOT['token']

bot1 = telepot.Bot(TOKEN)

@shared_task
def send_message(message_id, content):
    bot1.sendMessage(message_id, content)


@shared_task
def send_notice():
    message = """
*当前时时汇率如下，数据来自欧洲中央银行：*
"""
    for r in Rate.objects.all().order_by('sell_currency'):
        message += """
```
%(sell)s -> %(buy)s   %(price)s
```
        """ % {
            "sell": _(r.sell_currency),
            "buy": _(r.buy_currency),
            "price": r.price,
        }
        
    for u in TeleUser.objects.filter(subscribed=True):
        try:
            bot1.sendMessage(chat_id=u.chat_id, text=message, parse_mode="Markdown")
        except:
            print(u.chat_id)



bot2 = telepot.aio.DelegatorBot(TOKEN, [
   pave_event_space()(
       per_from_id(), create_open, MessageHandler, timeout=10),
])

@celeryd_init.connect
def start_message_loop(**kwargs):
    loop = asyncio.get_event_loop()
    loop.create_task(MessageLoop(bot2).run_forever())
    print('Listening ...')

    loop.run_forever()


def update_rate():
    c = CurrencyRates()
    arr = settings.SUPPORT_CURRENCIES

    h = {
        "USD": c.get_rates('USD'),
        "CNY": c.get_rates('CNY'),
        "PHP": c.get_rates('PHP'),
        "HKD": c.get_rates('HKD'),
    }

    for i in arr:
        for j in arr:
            if i != j:
                r, ok = Rate.objects.update_or_create(
                    sell_currency=i,
                    buy_currency=j,
                )
                r.price = h[i][j]
                r.save()

@shared_task
def send_bids_period():
    queryset =  Bid.objects.filter(user__is_blocked=False).order_by("sell_currency", "-date_created")
    message = """
*今天已有%s位商家报价：* 
    """ % queryset.count()
    for bid in queryset:
        message += """
`%(sell)s ``换 ``%(buy)s ``%(price)s `[%(short_name)s](tg://user?id=%(chat_id)s)
        """  % {
            "sell": _(bid.sell_currency),
            "buy": _(bid.buy_currency),
            "price": bid.price,
            "short_name": bid.user.name,
            "chat_id": bid.user.chat_id,
        }
    message += """
_北京时间24时自动清空数据，请各位商家每天发布一次最新报价。_
_换汇请注意安全，谨防诈骗。_
    """
    bot1.sendMessage(chat_id='-1001112269761', text=message, parse_mode="Markdown")