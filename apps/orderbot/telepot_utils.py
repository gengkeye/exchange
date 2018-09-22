# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import telepot
import re
import uuid
from django.conf import settings
from django.utils import timezone


from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError

from telepot.aio.helper import chat_flavors, inline_flavors
from telepot.namedtuple import (
    InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultCachedPhoto,
    InlineKeyboardMarkup, InlineKeyboardButton, ForceReply, ReplyKeyboardMarkup, KeyboardButton, 
)
from telepot.aio.helper import (
    UserHandler, InvoiceHandler, CallbackQueryOriginHandler, 
    InlineUserHandler, ChatHandler, Monitor, AnswererMixin
)
from orderbot.models import (
    TeleUser, TeleImage, TeleGroup, TeleMembership, TeleProduct, TeleStore, TeleBalanceHistory,
    TeleOrder, TeleOrderItem, Bid
)

class MessageHandler(UserHandler, AnswererMixin):
    def __init__(self, seed_tuple,
                 include_callback_query=True,
                 flavors=chat_flavors+inline_flavors, **kwargs):

        super(MessageHandler, self).__init__(seed_tuple,
                                            include_callback_query=True,
                                            flavors=chat_flavors+inline_flavors, **kwargs)
        self._bot = seed_tuple[0]

    @property
    def bot(self):
        return self._bot

    async def on_chat_message(self, msg):
        content_type, chat_type, chat_id, msg_date, msg_id = telepot.glance(msg, flavor='chat', long=True)
        group, user = self.get_group_and_user(msg)
        message =  _('tele_invalid_message')
        reply_markup = None
        if group:
            TeleMembership.objects.get_or_create(group=group, user=user)
        else:
            msg_id = None

        if content_type == 'text':
            text = msg['text']
            if text.startswith('/help'):
                message = _('help_message')
            elif text.startswith('/query'):
                message, reply_markup = self.query(user)
            elif text.startswith('/newbid'):
                message, reply_markup = self.new_bid(msg, group, user)
            elif text.startswith('/editbid'):
                message, reply_markup = self.edit_bid(text, group, user)
            elif text.startswith('/deletebid'):
                message, reply_markup = self.delete_bid(text, group, user)
            elif re.search('^[A-Z]{3}-[A-Z]{3}$', text):
                message = self.query_price(text, user)

        await self.bot.sendMessage(
            chat_id=chat_id,
            text=message,
            reply_markup=reply_markup,
            reply_to_message_id=msg_id,
            disable_notification=True,
            disable_web_page_preview=True,
            parse_mode="Markdown"
        )

    def on_chosen_inline_result(self, msg):
        result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
        print(self.id, ':', 'Chosen Inline Result:', result_id, from_id, query_string)

    async def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        print('Callback Query:', query_id, from_id, query_data)
        await self.bot.answerCallbackQuery(query_id, text='Got it')

    async def on_shipping_query(msg):
        query_id, from_id, invoice_payload = telepot.glance(msg, flavor='shipping_query')

        print('Shipping query:')
        print(query_id, from_id, invoice_payload)
        pprint(msg)
        print(ShippingQuery(**msg))

        await bot.answerShippingQuery(
            query_id, True,
            shipping_options=[
                ShippingOption(id='fedex', title='FedEx', prices=[
                    LabeledPrice(label='Local', amount=345),
                    LabeledPrice(label='International', amount=2345)]),
                ShippingOption(id='dhl', title='DHL', prices=[
                    LabeledPrice(label='Local', amount=342),
                    LabeledPrice(label='International', amount=1234)])])

    async def on_pre_checkout_query(msg):
        query_id, from_id, invoice_payload, currency, total_amount = telepot.glance(msg, flavor='pre_checkout_query', long=True)

        print('Pre-Checkout query:')
        print(query_id, from_id, invoice_payload, currency, total_amount)
        pprint(msg)
        print(PreCheckoutQuery(**msg))

        await bot.answerPreCheckoutQuery(query_id, True)


    def query(self, user):
        row1 = [
            KeyboardButton(
                text=_('PHP-CNY'),
            ),
            KeyboardButton(
                text=_('PHP-USD'),
            )
        ]
        row2 = [
            KeyboardButton(
                text=_('CNY-USD'),
            ),
            KeyboardButton(
                text=_('CNY-PHP'),
            )
        ]
        row3 = [
            KeyboardButton(
                text=_('USD-CNY'),
            ),
            KeyboardButton(
                text=_('USD-PHP'),
            )
        ]

        keyboard_buttons = ReplyKeyboardMarkup(
            keyboard = [row1, row2, row3],
            one_time_keyboard = False,
            selective=True
        )
        message = _('@%(username)s, please select currency pair.') % { "username": user.username }
        return message, keyboard_buttons


    def query_price(self, text, user):
        sell_currency, buy_currency = text.split('-')
        queryset =  Bid.objects.filter(
            sell_currency=sell_currency,
            buy_currency=buy_currency) \
            .order_by('sell_currency', "buy_currency", '-price')

        message = _("Latest price of %(sell_currency)s to %(buy_currency)s is as below:") % {
            "sell_currency": _(sell_currency),
            "buy_currency": _(buy_currency),
        } + "\n\n"

        message += """
```
%(price)s    %(amount)s    %(contact)s

```
        """ % {
            "price": _("Price"),
            "amount": _("Amount"),
            "contact": _("Contact"),
        }

        for bid in queryset:
            message += """
`%(price)s   ``%(amount)s   `[%(name)s](%(url)s)
            """  % {
                "price": bid.price,
                "amount": bid.max_amount,
                "name": user.name,
                "url": user.url
            }

        return message

    def new_bid(self, msg, group, user):
        row1 = [
            KeyboardButton(
                text=_('PHP-CNY'),
            ),
            KeyboardButton(
                text=_('PHP-USD'),
            )
        ]
        row2 = [
            KeyboardButton(
                text=_('CNY-USD'),
            ),
            KeyboardButton(
                text=_('CNY-PHP'),
            )
        ]
        row3 = [
            KeyboardButton(
                text=_('USD-CNY'),
            ),
            KeyboardButton(
                text=_('USD-PHP'),
            )
        ]

        keyboard_buttons = ReplyKeyboardMarkup(
            keyboard = [row1, row2, row3],
            one_time_keyboard = True,
            selective=True
        )
        return 'Send me your name', keyboard_buttons


    def edit_bid(self, text, group, user):
        pass

    def delete_bid(self, text, group, user):
        pass

    def get_group_and_user(self, msg, flavor='chat'):
        name = msg['from']['first_name']
        user_chat_id=msg['from']['id']
        try:
            username = msg['from']['username']
        except:
            username = None
        if flavor == 'inline_query':
            group = None
        elif flavor == 'chat': 
            content_type, chat_type, chat_id = telepot.glance(msg, 'chat')
            print("content_type:%s chat_type:%s chat_id:%s"%(content_type, chat_type, chat_id))
            if chat_type == 'private':
                group = None
            else:
                title = msg['chat']['title']
                group = self.get_and_update_or_create_group(title, chat_id)
        user = self.get_and_update_or_create_user(name, username, user_chat_id)
        return group, user
 
    def get_and_update_or_create_user(self, name, username, chat_id):
        try:
            user = TeleUser.objects.get(chat_id=chat_id)
        except:
            user = TeleUser.objects.create(chat_id=chat_id)
        else:
            if user.username != username:
                user.username = username
                user.save()

            if user.name != name:
                user.name = name
                user.save()
            return user  
            

    def get_and_update_or_create_group(self, title, chat_id):
        try:
            group = TeleGroup.objects.get(chat_id=chat_id)
            if group.title != title:
                group.title = title
                group.save()
        except:
            try:
                group = TeleGroup.objects.get(title=title)
                group.chat_id = chat_id
                group.save()
            except:
                try:
                    group = TeleGroup.objects.create(
                        title=title,
                        chat_id=chat_id,
                    )
                except:
                    from .tasks import send_error_info

                    send_error_info("ERROR: Create a group object failed.")
                    return None
        return group

