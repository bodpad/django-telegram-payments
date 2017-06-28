=====
Django Telegram Bot Payments (DTBP)
=====

It's easy way to set up a bot telegram and connect to the Django project for receiving payments.


Quick start
-----------

1. pip install django-telegram-payments

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

# bot436968383:AAHwxt5sI3imiY4l5oHIaUJceqCY80eFnAw
# 284685063:TEST:MjJmYWFkNmViZjhm