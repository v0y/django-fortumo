from django.core.urlresolvers import reverse
from django.test import (
    Client,
    TestCase,
)

from fortumo import consts
from fortumo.models import Message


class PaymentProcessorTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('payment_processor')
        self.valid_data = {
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
            'sig': '8d5714783f9cb60aa5798f892bbf3baf',
        }

    def test_successful_payment_process(self):
        response = self.client.get(self.url, self.valid_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'dummy')

        message = Message.objects.get()
        self.assertEqual(message.sig, '8d5714783f9cb60aa5798f892bbf3baf')

    def test_unsuccessful_payment_process_invalid_signature(self):
        invalid_data = self.valid_data.copy()
        invalid_data['sig'] = '666'
        response = self.client.get(self.url, invalid_data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Message.objects.count(), 0)
