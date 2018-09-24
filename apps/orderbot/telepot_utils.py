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
    MessageEntity
)
from telepot.aio.helper import (
    UserHandler, InvoiceHandler, CallbackQueryOriginHandler, 
    InlineUserHandler, ChatHandler, Monitor, AnswererMixin
)
from orderbot.models import TeleUser, TeleImage, TeleGroup, TeleMembership, Bid

wizards = {}

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

        # init
        message =  _('tele_invalid_message')
        reply_markup = None
        parse_mode = None

        if group:
            TeleMembership.objects.get_or_create(group=group, user=user)
        else:
            msg_id = None
        
        rows = []
        allc = settings.SUPPORT_CURRENCIES
        for i in allc:
            cols = []
            for j in allc:
                if j != i:
                    cols.append(
                        KeyboardButton(
                            text='%s-%s'%(i, j),
                        )
                    )
            rows.append(cols)

        default_reply_markup = ReplyKeyboardMarkup(
            keyboard = rows,
            one_time_keyboard = False,
            selective=True
        )
        if content_type == 'text':
            text = msg['text']
            if text.startswith('/help'):
                message = _('help_message')
            elif text.startswith('/query'):
                message = _("@%(username)s, please select currency pair.") % { "username": user.username }
                reply_markup = default_reply_markup

            elif text.startswith('/newbid'):
                message = self.new_bid_command(group, user)
                reply_markup = default_reply_markup

            elif text.startswith('/editbid'):
                message = self.edit_bid_command(text, group, user)

            elif text.startswith('/deletebid'):
                message = self.delete_bid_command(text, group, user)

            else:
                try:
                    message = self.plain_text(text, user)
                except:
                    if re.search('^[A-Z]{3}-[A-Z]{3}$', text):
                        message = self.query_price(text, user)
                        reply_markup = default_reply_markup
                        parse_mode="Markdown"

        await self.bot.sendMessage(
            chat_id=chat_id,
            text=message,
            reply_markup=reply_markup,
            reply_to_message_id=msg_id,
            disable_notification=True,
            disable_web_page_preview=True,
            parse_mode=parse_mode
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
%(price)s       %(amount)s       %(contact)s

```
        """ % {
            "price": _("Price"),
            "amount": _("Amount"),
            "contact": _("Contact"),
        }

        for bid in queryset:
            message += """
`%(price)s%(pspace)s``%(amount)s%(aspace)s`[%(name)s](%(url)s)
            """  % {
                "price": bid.price,
                "pspace":" "*(10-len(str(bid.price))),
                "amount": bid.max_amount,
                "aspace":" "*(10-len(str(bid.max_amount))),
                "name": user.name,
                "url": user.url,
            }

        return message

    def plain_text(self, text, user):
        chatId = user.chat_id
        h = wizards[chatId]
        if len(h["conditions"]) > 0:
            if re.search(h['conditions'][-1], text):
                h['conditions'].pop()
                h["rtn_err_msgs"].pop()
                h['msg_arr'].append(text)
                if len(h['conditions']) == 0:
                    if h["type"] == "newbid":
                        sell_currency, buy_currency = h['msg_arr'][0].split('-')
                        Bid.objects.create(
                            sell_currency=sell_currency,
                            buy_currency=buy_currency,
                            max_amount=h['msg_arr'][1],
                            price=h['msg_arr'][2],
                            user=user
                        )
                    elif h["type"] == "editbid":
                        pass
                    elif h["type"] == "deletebid":
                        pass

                return h["rtn_msgs"].pop()
            else:
                return h["rtn_err_msgs"][-1]

        else:
            h.clear()
            raise "hi,ann"


    def new_bid_command(self, group, user):
        if group:
            return _('You should do this in private chat with me.')
        else:
            wizards[user.chat_id] = {
                "type": 'newbid',
                "conditions": [
                    '^[-+]?[0-9]*\.?[0-9]{1,2}$',
                    '^[1-9][0-9]{1,7}$',
                    '^[A-Z]{3}-[A-Z]{3}$'
                ],
                "rtn_msgs": [
                    _("Congratulations, you created a new bid successfully!"),
                    _("please send me your price"),
                    _("please send me your currency amount"),
                ],
                "rtn_reply_markup": [None, None, None],
                "rtn_err_msgs": [ 
                    _("Price must be a float number within two decimal places."), 
                    _("Amount must be an integer between 10 and 10 millions."),
                    _("please tap the keyboard below to select."),
                ],
                "msg_arr": [],
            }
            return _("@%(username)s, you're creating a new bid, please tap keyboard to select a currency pair firstly.") % { "username": user.username }


    def edit_bid_command(self, text, group, user):
        pass

    def delete_bid_command(self, text, group, user):
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

