from django import forms


class BotCreatingForm(forms.Form):
    bot_token = forms.CharField(
        label='Bot authentication token, obtained via @BotFather',
        required=True
    )

    payments_provider_token = forms.CharField(
        label='Payments provider token, obtained via @BotFather',
        required=True
    )

    func = forms.CharField(
        label='Created definition like package.module.def',
        required=True
    )


class BotSettingsForm(forms.Form):
    onoff = forms.BooleanField(required=False)

    need_name = forms.BooleanField(
        required=False,
        help_text="If you require the user's full name to complete the order"
    )

    need_phone_number = forms.BooleanField(
        required=False,
        help_text="If you require the user's phone number to complete the order"
    )

    need_email = forms.BooleanField(
        required=False,
        help_text="If you require the user's email to complete the order"
    )

    need_shipping_address = forms.BooleanField(
        required=False,
        help_text="If you require the user's shipping address to complete the order"
    )

    message_if_bot_is_disabled = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2})
    )

