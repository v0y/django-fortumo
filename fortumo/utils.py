import hashlib

from django.conf import settings


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

    return hashlib.md5(calculation_string).hexdigest()
