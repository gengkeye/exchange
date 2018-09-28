# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import telepot
import re
import uuid
from django.conf import settings
from django.utils import timezone
from time import sleep

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
from telepot.text import apply_entities_as_markdown
from .utils import get_object_or_none
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
        message =  ''
        reply_markup = None
        parse_mode = None
        rtn_id = chat_id

        if group:
            TeleMembership.objects.get_or_create(group=group, user=user)
        else:
            msg_id = None
        
        rows = []
        allc = settings.SUPPORT_CURRENCIES
        for i in allc:
            rows.append([
                KeyboardButton(
                    text=i,
                )
            ])

        default_reply_markup = ReplyKeyboardMarkup(
            keyboard = rows,
            one_time_keyboard = False,
            selective=True
        )
        if content_type == 'text':
            text = msg['text']
            if text.startswith('/help'):
                try:
                    wizards[user.chat_id].clear()
                except:
                    pass 
                if group:
                    message += """


            
`-发布个人报价点击` [@oldsevenbot](https://telegram.me/oldsevenbot)

`-查看全部报价点击` [/query](tg:///query)

`-查看个人报价点击` [/list](tg:///list)

`本机器人，仅提供统计，所有人均可自由、免费发布信息，`

`只为协助群友找到好的买卖。换汇仍请小心，注意诈骗。`
"""
                else:
                    message = apply_entities_as_markdown(_("help_message"), [{"offset":1, "length":10, "type": "bold"}])
                reply_markup = ReplyKeyboardMarkup(
                    keyboard = [
                        [KeyboardButton(text='/query 查看报价')],
                        [KeyboardButton(text='/list 查看我的报价记录')],
                        [KeyboardButton(text='/new 发布报价')],
                    ],
                    one_time_keyboard = False,
                    selective=True
                )
                parse_mode="Markdown"
            elif text.startswith('/query'):
                try:
                    wizards[user.chat_id].clear()
                except:
                    pass 
                message = _("@%(username)s, please select currency pair.") % { "username": user.username }
                reply_markup = default_reply_markup

            elif text.startswith('/list'):
                try:
                    wizards[user.chat_id].clear()
                except:
                    pass
                message = self.list_command(user)
                rtn_id = user.chat_id
                parse_mode="Markdown"
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(text=_('clear'), callback_data="/clear"),
                        ],
                    ]
                )

            elif text.startswith('/new'):
                try:
                    wizards[user.chat_id].clear()
                except:
                    pass 
                if group:
                    message = _('You should do this in private chat with me.')
                else:
                    message = self.new_command(user)
                    reply_markup = default_reply_markup

            else:
                try:
                    message = self.plain_text(text, user)
                except:
                    try:
                        wizards[user.chat_id].clear()
                    except:
                        pass
                    if re.search('^[A-Z]{3}$', text.strip()):
                        message = self.query_price(text.strip(), group, user)
                        parse_mode="Markdown"

        if message:
            await self.bot.sendMessage(
                chat_id=rtn_id,
                text=message,
                reply_markup=reply_markup,
                reply_to_message_id=msg_id,
                disable_notification=False,
                disable_web_page_preview=False,
                parse_mode=parse_mode
            )

    def on_chosen_inline_result(self, msg):
        result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
        print(self.id, ':', 'Chosen Inline Result:', result_id, from_id, query_string)

    async def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        print('Callback Query:', query_id, from_id, query_data)
        user = get_object_or_none(TeleUser, chat_id=from_id)
        if user:
            user.bids.all().delete()

        await self.bot.answerCallbackQuery(query_id, text=_('Already cleared'))

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


    def query_price(self, text, group, user):
        sell_currency = text.strip()
        queryset =  Bid.objects.filter(sell_currency=sell_currency) \
            .order_by("-date_created", "buy_currency")[:50]

        message = """
```
 %(sell)s    %(buy)s  %(price)s    %(contact)s
```
        """ % {
            "sell": _("OUT"),
            "buy": _("IN"),
            "price": _("Price"),
            "amount": _("Amount"),
            "contact": _("Contact"),
        }

        for bid in queryset:
            message += """
`%(sell)s%(sspace)s``%(buy)s%(bspace)s``%(price)s%(pspace)s`[%(short_name)s](tg://user?id=%(chat_id)s)
            """  % {
                "sell": _(bid.sell_currency),
                "sspace": " "*(7-2*(len(bid.sell_currency))),
                "buy": _(bid.buy_currency),
                "bspace": " "*(7-2*(len(bid.buy_currency))),
                "price": bid.price,
                "pspace":" "*(7-len(str(bid.price))),
                "short_name": bid.user.short_name,
                "chat_id": bid.user.chat_id,
            }

        if group:
            message += """



`-发布个人报价点击` [@oldsevenbot](https://telegram.me/oldsevenbot)

`-查看全部报价点击` [/query](tg:///query)

`-查看个人报价点击` [/list](tg:///list)

`本机器人，仅提供统计，所有人均可自由、免费发布信息，`

`只为协助群友找到好的买卖。换汇仍请小心，注意诈骗。`
"""
        else:
            message += "\n\n" + apply_entities_as_markdown(_("help_message"), [{"offset":1, "length":10, "type": "bold"}])

        return message

    def plain_text(self, text, user):
        chatId = user.chat_id
        h = wizards[chatId]
        if len(h["conditions"]) > 0:
            if re.search(h['conditions'][-1], text):
                h['conditions'].pop()
                h["rtn_err_msgs"].pop()
                h['msg_arr'].append(text)
                if len(h['conditions']) == 0 and  h["type"] == "new" and h['msg_arr'][0] != h['msg_arr'][1]:
                    Bid.objects.filter(
                        sell_currency=h['msg_arr'][0],
                        buy_currency=h['msg_arr'][1],
                        user=user).delete()
                    Bid.objects.create(
                        sell_currency=h['msg_arr'][0],
                        buy_currency=h['msg_arr'][1],
                        price=h['msg_arr'][2],
                        user=user
                    )
                return h["rtn_msgs"].pop()
            else:
                return h["rtn_err_msgs"][-1]

        else:
            h.clear()
            raise "ERROR"

    def list_command(self, user):
        queryset =  Bid.objects.filter(user=user).order_by("-date_created")
        message = """
```
%(sell)s  %(buy)s  %(price)s      %(date)s
```
        """ % {
            "sell": _("Sell"),
            "buy": _("Buy"),
            "price": _("Price"),
            "date": _("Date"),
        }

        for bid in queryset:
            message += """
`%(sell)s  ``%(buy)s  ``%(price)s%(pspace)s``%(date)s`
            """  % {
                "sell": bid.sell_currency,
                "buy": bid.buy_currency,
                "price": bid.price,
                "pspace":" "*(8-len(str(bid.price))),
                "date":bid.date_created.date(),
            }

        return message

    def new_command(self, user):
        wizards[user.chat_id] = {
            "type": 'new',
            "conditions": [
                '^[-+]?[0-9]*\.?[0-9]{1,2}$',
                '^[A-Z]{3}$',
                '^[A-Z]{3}$',
            ],
            "rtn_msgs": [
                _("Congratulations, you created a new bid successfully!") + "\n\n\n" + _("help_message"),
                _("please send me your price"),
                _("please send me the currency you wanna buy"),
            ],
            "rtn_err_msgs": [ 
                _("Price must be a float number within two decimal places."), 
                _("please tap the keyboard below to select."),
                _("please tap the keyboard below to select."),
            ],
            "msg_arr": [],
        }
        return _("please send me the currency you wanna sell") % { "username": user.username }


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
            user = TeleUser.objects.create(chat_id=chat_id, name=name, username=username)
        
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

