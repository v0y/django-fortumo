from django.db import models


class Message(models.Model):
    message = models.CharField(max_length=64)
    sender = models.CharField(max_length=64, db_index=True)
    country = models.CharField(max_length=2)
    price = models.FloatField()
    price_wo_vat = models.FloatField()
    currency = models.CharField(max_length=3)
    service_id = models.CharField(max_length=128)
    message_id = models.CharField(max_length=128)
    keyword = models.CharField(max_length=64)
    shortcode = models.CharField(max_length=64)
    operator = models.CharField(max_length=128)
    billing_type = models.CharField(max_length=2)
    status = models.CharField(max_length=64)
    test = models.CharField(max_length=16)
    sig = models.CharField(max_length=128)
