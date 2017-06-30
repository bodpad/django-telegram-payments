=====
Django Telegram Bot Payments (DTBP) =>In developing<=
=====

It's easy way to set up a bot telegram and connect to the Django project for receiving payments.


Quick start
-----------

1. pip install git+https://github.com/bodpad/django-telegram-payments.git

1. Add "telegram_payments" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'telegram_payments',
    ]

2. Include the DTBP URLconf in your project urls.py like this::

    url(r'^dtbp/', include('telegram_payments.urls')),

3. Visit http://127.0.0.1:8000/dtbp/

4. ...

5. ...


Supported languages: En, Ru