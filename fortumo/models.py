from django.db import models
from json_field import JSONField


class Service(models.Model):
    name = models.CharField(max_length=64)
    secret = models.CharField(max_length=128)
    service_id = models.CharField(max_length=128)
    ips = JSONField(default=[])
    validate_ip = models.BooleanField(default=True)

    def __str__(self):
        return self.name


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

    def __str__(self):
        return '{} - {} from {} on {}'.format(
            self.keyword,
            self.message,
            self.sender,
            self.shortcode,
        )


class Payment(models.Model):
    service = models.ForeignKey(Service, related_name='payments')
    message = models.OneToOneField(Message)
    pin = models.CharField(max_length=16, unique=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return '{} - {}'.format(self.id, self.pin)
