import json
import shelve

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.utils.translation import ugettext as _
from .forms import BotCreatingForm, BotSettingsForm
from .bot import TelegramBotPayments, create_bot, DB_FILEPATH


@require_http_methods(["GET"])
def main(request):
    bot = TelegramBotPayments()
    return redirect('dtbp_create') if bot.token is None else redirect('dtbp_settings')


@user_passes_test(lambda u: u.is_superuser)
def settings(request):
    """
    Bot settings view
    """
    bot = TelegramBotPayments()

    if bot.token is None:
        return redirect('dtbp_create')

    if request.method == 'GET':
        initial = dict()

        db = shelve.open(DB_FILEPATH)
        initial.update({'onoff': db.get('onoff')})
        initial.update({'need_name':  db.get('need_name')})
        initial.update({'need_phone_number': db.get('need_phone_number')})
        initial.update({'need_email': db.get('need_email')})
        initial.update({'need_shipping_address': db.get('need_shipping_address')})
        initial.update({'message_if_bot_is_disabled': db.get('message_if_bot_is_disabled')})
        db.close()

        context = {
            'form': BotSettingsForm(initial=initial),
            'bot': bot,
        }

        return render(request, 'telegram_payments/main.html', context)
    else:
        form = BotSettingsForm(request.POST)

        if not form.is_valid():
            return render(request, 'telegram_payments/main.html', {'form': form, 'bot': bot})

        # Updating bot settings
        with shelve.open(DB_FILEPATH) as db:
            db['onoff']                      = form.cleaned_data['onoff']
            db['need_name']                  = form.cleaned_data['need_name']
            db['need_phone_number']          = form.cleaned_data['need_phone_number']
            db['need_email']                 = form.cleaned_data['need_email']
            db['need_shipping_address']      = form.cleaned_data['need_shipping_address']
            db['message_if_bot_is_disabled'] = form.cleaned_data['message_if_bot_is_disabled']
            db.close()

        return redirect('dtbp_settings')


@user_passes_test(lambda u: u.is_superuser)
def create(request):
    """
    Bot creating view
    """
    if request.method == 'GET':
        form = BotCreatingForm()
        return render(request, 'telegram_payments/create.html', {'form': form})
    else:
        form = BotCreatingForm(request.POST)

        if not form.is_valid():
            # If the form is not valid, display errors.
            return render(request, 'telegram_payments/create.html', {'form': form})

        # Bot token
        # https://core.telegram.org/bots/api#authorizing-your-bot
        token = form.cleaned_data['bot_token']

        # Payments provider token
        # https://core.telegram.org/bots/payments#getting-a-token
        provider_token= form.cleaned_data['payments_provider_token']

        # Custom function for obtaining order data.
        function = form.cleaned_data['func']

        # Url for receive incoming updates via an outgoing webhook.
        # https://core.telegram.org/bots/api#setwebhook
        webhook = reverse('dtbp_webhook', args=[token])
        webhook = request.build_absolute_uri(webhook)

        # Creating a bot
        create_bot(token, provider_token, webhook, function)

        return redirect('dtbp_settings')


@csrf_exempt
def webhook(request, bot_token):
    # request_body = json.loads(request.body)
    request_body = '{"update_id":263998294,\n"message":{"message_id":160,"from":{"id":63308080,"first_name":"Kalamart","username":"kalamartru","language_code":"ru-RU"},"chat":{"id":63308080,"first_name":"Kalamart","username":"kalamartru","type":"private"},"date":1498458475, "text":"/pay 35"}}'
    request_body = json.loads(request_body)

    error_message = _("Unknown command.\nPlease enter\n<b>/pay [order number]</b>\nfor payment.")

    message = request_body['message']

    # Unique chat identifier between user and bot.
    chat_id = message['chat']['id']

    bot = TelegramBotPayments(chat_id)

    # Request comes not from Telegram
    if bot.token != bot_token:
        return HttpResponse()

    if not bot.is_on():
        bot.send_message(bot.message_if_disabled)
        return HttpResponse()

    # The message that the user sent to the bot
    text = message.get('text')

    # text is None, если боту отправили не текстовове сообщение (sticker, video, location e.t.c.)
    if text is None:
        bot.send_message(error_message)
        return HttpResponse()

    try:
        command, order_id = text.lower().split(' ', 1)
    except ValueError:
        bot.send_message(error_message)
        return HttpResponse()

    comands_i18n = ['/pay', '/оплатить']

    if command not in comands_i18n or not order_id.isdigit():
        bot.send_message(error_message)
        return HttpResponse()

    get_data = bot.get_func()
    data = get_data(request, order_id)

    if data is None:
        # Пользовательская функция ничего не вернула
        bot.send_message("Order #{0} not found.".format(order_id))
        return HttpResponse()

    bot.send_invoice(
        order_id=order_id,
        description=data['description'],
        prices=data['prices']
    )

    return HttpResponse()


@user_passes_test(lambda u: u.is_superuser)
@require_http_methods(["POST"])
def delete(request):
    """
    Bot deleting view
    """
    bot = TelegramBotPayments()
    bot.clear()
    return redirect('dtbp_settings')