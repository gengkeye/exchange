# ~*~ coding: utf-8 ~*~
#
from __future__ import absolute_import

from celery import shared_task
from celery.signals import celeryd_init
from django.conf import settings
from config import env
from django.utils.translation import ugettext as _

from orderbot.models import TeleGroup, TeleOrder, TeleMembership
import telepot
import asyncio
from telepot.aio.loop import MessageLoop
from telepot.aio.delegate import pave_event_space, create_open, per_from_id
from .telepot_utils import MessageHandler

TOKEN = settings.TELEGRAM_BOT['token']

bot1 = telepot.Bot(TOKEN)

@shared_task
def send_message(message_id, content):
	bot1.sendMessage(message_id, content)


@shared_task
def send_group_notice(text):
	for group in TeleGroup.objects.all():
		try:
			bot1.sendMessage(group.chat_id, text[7:])
		except:
			pass

@shared_task
def  send_order_notice(order_id):
	try:
		order = TeleOrder.objects.get(id=order_id)
		message = order.summary()
		bot1.sendMessage(order.group.driver.chat_id, message) # order.store.owner.chat_id
		print('Send order notice successfully.')
	except:
		print('Send order notice failed.')

@shared_task
def notice_openorder(group_id):
	for m in TeleMembership.objects.filter(group__id=group_id, subscribed=True):
		try:
			bot1.sendMessage(m.user.chat_id, _("Hello %(name)s, I'm glad to notice you: %(groupname)s is ready to order meal.")% \
			    { "name": m.user.name, "groupname": group.title })
		except:
			pass


@shared_task
def send_error_info(err):
	admin = TeleUser.objects.filter(role='Admin').get()
	bot1.sendMessage(admin.chat_id, err)


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