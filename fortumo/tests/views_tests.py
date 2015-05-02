from unittest import TestCase

from django.core.urlresolvers import reverse
from django.test import Client

from fortumo import consts
from fortumo.models import Message


class PaymentProcessorTestCase(TestCase):

    def test_successful_process(self):
        client = Client()
        url = reverse('payment_processor')
        get_data = {
            'message': '123',
            'sender': '358401234567',
            'country': 'SE',
            'price': 0.32,
            'price_wo_vat': 0.27,
            'currency': 'SEK',
            'service_id': 'f7fa12b381d290e268f99e382578d64a',
            'message_id': '123456',
            'keyword': 'KEY',
            'shortcode': 1311,
            'operator': 'Vodafone',
            'billing_type': consts.BillingType.MO,
            'status': consts.Status.OK,
            'test': consts.Test.FALSE,
            'sig': '2d7b58632d855bf031af5066761f25cd',
        }
        response = client.get(url, get_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'dummy')

        message = Message.objects.get()
        self.assertEqual(message.sig, '2d7b58632d855bf031af5066761f25cd')
