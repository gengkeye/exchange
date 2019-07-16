# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import telepot
import requests
import re
import time

from django.utils.translation import ugettext as _

from telepot.aio.helper import chat_flavors, inline_flavors
from telepot.aio.helper import UserHandler, AnswererMixin
from telepot.text import apply_entities_as_markdown
from .utils import get_object_or_none, trans, convert_str_to_list
from exchange.models import TeleUser, TeleGroup, TeleMembership, Bid, Rate

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
        message = parse_mode = None
        rtn_id = chat_id

        if group:
            TeleMembership.objects.get_or_create(group=group, user=user)
        else:
            msg_id = None
            user.subscribed = True
            user.save()

        if content_type == 'text':
            text = msg['text']
            if group.ban_keywords and re.search(group.ban_keywords, text):
                message = "delete"
            else:
                message = self.plain_text(text, user, group)
                parse_mode = "Markdown"

        elif content_type == 'new_chat_member':
            name = ''
            for m in msg['new_chat_members']:
                name += m['first_name'] + ','
            message = "%s 欢迎加入本群！" % name

        if message:
            if message == 'delete':
                await self.bot.deleteMessage(msg_id)
            else:
                await self.bot.sendMessage(
                    chat_id=rtn_id,
                    text=message,
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


    def query_price(self, text, user):
        queryset =  Bid.objects.filter(sell_currency=trans(text)) \
            .order_by("-date_created", "buy_currency")
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
        return message


    def plain_text(self, text, user, group):
        text_arr = convert_str_to_list(text)
        message = None
        if text_arr[0] == '屏蔽':
            if user.is_admin:
                group.ban_keywords = "|".join(a[1:])
                group.save()
                message = _("Ban successfully!")
            else:
                message = _("Permission Denied")

        elif len(text_arr) == 1:
            if trans(text_arr[0]):
                message = self.query_price(text_arr[0], user)

            elif text_arr[0] in ['即时汇率', '汇率']:
                rates = Rate.objects.all().order_by('sell_currency')
                message = """
*当前时时汇率如下，数据来自欧洲中央银行*
_更新时间：%s_
                """ % rates.first().date_created
                for r in rates:
                    message += """
```
%(sell)s -> %(buy)s   %(price)s
```
                """ % {
                    "sell": _(r.sell_currency),
                    "buy": _(r.buy_currency),
                    "price": r.price,
                }

            elif text_arr[0] == '报价':
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
                
            elif text_arr[0] == '我的报价':
                queryset =  Bid.objects.filter(user=user).order_by("sell_currency", "-date_created")
                if queryset:
                    message = """
*%s，您所有的报价如下：*
                    """ % user.name
                    for bid in queryset:
                        message += """
`%(sell)s ``换 ``%(buy)s ``%(price)s ``%(date)s`
                        """  % {
                            "sell": _(bid.sell_currency),
                            "buy": _(bid.buy_currency),
                            "price": bid.price,
                            "date": bid.date_created.date()
                        }
                else:
                    message = "_%s，您没有报价记录！_" % user.name
            elif text_arr[0] == '币价':
                message = """
```
当前排行前30的虚拟货币价格如下，数据来自coinmarketcap.com
```
                """
                response = requests.get('https://api.coinmarketcap.com/v2/ticker/?limit=30')
                if response:
                    data = response.json()['data']
                    for key in data.keys():
                        message += """
`%(symbol)s`    `$%(price)s` 
                        """ % {
                            "symbol": data[key]['symbol'],
                            "price": data[key]['quotes']['USD']['price'],
                        }



            elif text_arr[0] == '清空报价':
                Bid.objects.filter(user=user).delete()
                message = "_%s，已清空您的所有报价！_" % user.name

            elif text_arr[0] == '帮助':
                message = _("help_message")

        if len(text_arr) == 2:
            if text_arr[0] == '删除报价' and trans(text_arr[1]):
                Bid.objects.filter(user=user, sell_currency=trans(text_arr[1])).delete()
                message = "_%s，已删除您所有%s的报价！_" % (user.name, text_arr[1])

            if text_arr[0] == 'block' and user.role == 'Admin':
                TeleUser.objects.filter(name=text_arr[1]).update(is_blocked=True)
                message = "%s was blocked" % text_arr[1]

        if len(text_arr) == 3:
            sell = trans(text_arr[0])
            buy = trans(text_arr[1])
            price = text_arr[2]
            if sell and buy and re.search('^[-+]?[0-9]*\.?[0-9]{1,2}$', price):
                Bid.objects.filter(sell_currency=sell, buy_currency=buy, user=user).delete()
                Bid.objects.create(sell_currency=sell, buy_currency=buy, price=price, user=user)
                message = apply_entities_as_markdown(_("you created a new bid successfully!"), [{"offset":1, "length":10, "type": "bold"}])
        return message


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
            user.username = str(username)
            user.save()

        if user.name != str(name):
            user.name = str(name)
            user.save()

        return user  
            

    def get_and_update_or_create_group(self, title, chat_id):
        try:
            group = TeleGroup.objects.get(chat_id=chat_id)
            if group.title != str(title):
                group.title = str(title)
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
                    return None
        return group

