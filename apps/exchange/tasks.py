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
