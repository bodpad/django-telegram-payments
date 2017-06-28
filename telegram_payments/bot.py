import json
import os
import shelve
import requests
import importlib
from django.conf import settings
from django.utils.translation import ugettext as _

API_URL = 'https://api.telegram.org/bot{0}/{1}'
DB_FILEPATH = os.path.join(settings.MEDIA_ROOT, 'dtbp')


def create_bot(bot_token, payments_provider_token, webhook_url, function):
    # Set webhook
    request_url = API_URL.format(bot_token, 'setWebhook')
    request = requests.post(request_url, data={'url': webhook_url})

    # Getting bot username from Telegram API
    request_url = API_URL.format(bot_token, 'getMe')
    result = requests.get(request_url)
    username = result.json()['result']['username']

    with shelve.open(DB_FILEPATH) as db:
        db['bot_token'] = bot_token
        db['bot_username'] = username
        db['payments_provider_token'] = payments_provider_token
        db['function'] = function
        db['message_if_bot_is_disabled'] = _("We're sorry, but we can't send your payment right now.")
        db['need_name'] = False
        db['need_phone_number'] = False
        db['need_email'] = False
        db['functneed_shipping_addression'] = False
        db['onoff'] = False
        db.close()


class TelegramBotPayments:

    def __init__(self, chat_id=None):
        if not chat_id is None:
            self.chat_id = chat_id
        with shelve.open(DB_FILEPATH) as db:
            self.token = db.get('bot_token')
            self.username = db.get('bot_username')
            self.pp_token = db.get('payments_provider_token')
            db.close()

    def is_on(self):
        with shelve.open(DB_FILEPATH) as db:
            return db.get('onoff')

    def turn_on(self):
        with shelve.open(DB_FILEPATH) as db:
            db['onoff'] = True
            db.close()

    def turn_off(self):
        with shelve.open(DB_FILEPATH) as db:
            db['onoff'] = False
            db.close()

    def clear(self):
        with shelve.open(DB_FILEPATH) as db:
            db.clear()
            db.close()

    def set_message_if_bot_is_disabled(self, message):
        with shelve.open(DB_FILEPATH) as db:
            db['message_if_bot_is_disabled'] = message
            db.close()

    def get_message_if_bot_is_disabled(self):
        with shelve.open(DB_FILEPATH) as db:
            return db.get('message_if_bot_is_disabled')

    def send_invoice(self, order_id: int, description: str, prices: list):
        db = shelve.open(DB_FILEPATH)

        data = {
            'chat_id': self.chat_id,
            'title': _('Payment order #') + str(order_id),
            'description': description,
            'payload': 1,
            'provider_token': self.pp_token,
            'start_parameter': order_id,
            'currency': _('USD'),
            'prices': json.dumps(prices),
            'need_phone_number': db.get('need_phone_number', False),
            'need_name': db.get('need_name', False),
            'need_email': db.get('need_email', False),
            'need_shipping_address': db.get('need_shipping_address', False),
            'is_flexible': db.get('is_flexible', False)
        }

        url = API_URL.format(self.token, 'sendInvoice')
        request = requests.post(url, data=data)
        #print(r.request.body)
        #print(r.text)

    def send_message(self, text:str):
        url = API_URL.format(self.token, 'sendMessage')
        data = {
            'chat_id': self.chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        request = requests.post(url, data=data)

        if request.status_code:
            print(request.text)


    # def get_cc(self):
    #     try:
    #         from django.conf import settings
    #         cc = settings.LANGUAGE_CODE.split('-')[1].lower()
    #     except:
    #         cc = 'en'
    #     else:
    #         return cc

    def get_func(self):
        try:
            with shelve.open(DB_FILEPATH) as db:
                name = db['function']
                db.close()

            p, d = name.rsplit('.', 1)
            mod = importlib.import_module(p)
            return getattr(mod, d)
        except:
            print('Попытка импорта не удалась')
            return None