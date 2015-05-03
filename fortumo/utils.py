import hashlib
from random import randint

from django.conf import settings
from fortumo.models import Payment


def calculate_signature(data):
    """
    https://developers.fortumo.com/mobile-payments-api/security/
    """
    calculation_string = ''.join([
        '{}={}'.format(k, v)
        for k, v
        in sorted(data.items())
        if k != 'sig'
    ])
    calculation_string = '{}{}'.format(
        calculation_string,
        settings.FORTUMO_SECRET,
    )

    return hashlib.md5(calculation_string.encode('utf-8')).hexdigest()


def signature_is_valid(data):
    signature = data['sig']
    return calculate_signature(data) == signature


def generate_pin():
    pin = '{}-{}'.format(
        str(randint(0, 999)).zfill(3),
        str(randint(0, 999)).zfill(3),
    )
    return pin


def generate_unique_pin(service_id):
    used_pins = Payment.objects \
        .filter(used=False, service__service_id=service_id) \
        .values_list('pin', flat=True)

    pin = generate_pin()
    while pin in used_pins:
        pin = generate_pin()

    return pin
