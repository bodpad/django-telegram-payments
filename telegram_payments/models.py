from django.db import models
from django.urls import reverse


# class TelegramPaymentBot(models.Model):
#     name = models.CharField(max_length=255)
#     token = models.CharField(max_length=255)
#     handler = models.URLField()
#     on = models.BooleanField(default=False)
#
#     def get_absolute_url(self):
#         return reverse('bot_detail', args=[str(self.name)])