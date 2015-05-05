from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import (
    Client,
    TestCase,
)
from mock import patch

from fortumo import consts
from fortumo.models import (
    Message,
    Payment,
    Service,
)


class BaseViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
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
        self.service = Service.objects.create(
            service_id='f7fa12b381d290e268f99e382578d64a',
            secret='123',
            validate_ip=False,
        )


class PaymentProcessorTestCase(BaseViewTestCase):

    def setUp(self):
        super(PaymentProcessorTestCase, self).setUp()
        self.url = reverse('payment_processor')

    def _mock_generate_pin(*args, **kwargs):
        return '111-111'

    @patch('fortumo.utils.generate_pin', _mock_generate_pin)
    def test_successful_payment_process(self):
        response = self.client.get(self.url, self.valid_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'111-111')
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Payment.objects.count(), 1)

    def test_unsuccessful_payment_process_invalid_signature(self):
        self.valid_data['sig'] = '666'
        response = self.client.get(self.url, self.valid_data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(Payment.objects.count(), 0)

    def test_unsuccessful_payment_process_invalid_ip(self):
        settings.FORTUMO_IPS = []
        response = self.client.get(self.url, self.valid_data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(Payment.objects.count(), 0)


class CheckPinTestCase(BaseViewTestCase):

    def setUp(self):
        super(CheckPinTestCase, self).setUp()
        self.url = reverse('check_pin')
        message = Message.objects.create(**self.valid_data)
        self.payment = Payment.objects.create(
            service=self.service,
            message=message,
            pin='111-111',
        )

    def test_valid_pin(self):
        post_data = {
            'secret': '123',
            'pin': '111-111'
        }
        response = self.client.post(self.url, post_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content.decode('utf-8'),
            consts.PinResponse.VALID,
        )
        payment = Payment.objects.get()
        self.assertTrue(payment.used)

    def test_invalid_pin(self):
        post_data = {
            'secret': '123',
            'pin': '222-222'
        }
        response = self.client.post(self.url, post_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content.decode('utf-8'),
            consts.PinResponse.INVALID,
        )
        payment = Payment.objects.get()
        self.assertFalse(payment.used)

    def test_invalid_secret(self):
        post_data = {
            'secret': '666',
            'pin': '111-111'
        }
        response = self.client.post(self.url, post_data)
        self.assertEqual(response.status_code, 403)
        payment = Payment.objects.get()
        self.assertFalse(payment.used)


class CheckPinIpValidationTestCase(BaseViewTestCase):

    def setUp(self):
        super(CheckPinIpValidationTestCase, self).setUp()
        self.url = reverse('check_pin')

    def test_check_pin_with_invalid_ip(self):
        service = Service.objects.create(
            service_id='100',
            secret='200',
            ips=['256.256.256.256'],
            validate_ip=True,
        )
        message = Message.objects.create(**self.valid_data)
        Payment.objects.create(
            service=service,
            message=message,
            pin='111-111',
        )
        post_data = {'secret': '200', 'pin': '111-111'}
        response = self.client.post(self.url, post_data)
        self.assertEqual(response.status_code, 403)
        payment = Payment.objects.get()
        self.assertFalse(payment.used)

    def test_check_pin_with_valid_ip(self):
        service = Service.objects.create(
            service_id='100',
            secret='200',
            ips=['127.0.0.1'],
            validate_ip=True,
        )
        message = Message.objects.create(**self.valid_data)
        Payment.objects.create(
            service=service,
            message=message,
            pin='555-666',
        )
        post_data = {'secret': '200', 'pin': '555-666'}
        response = self.client.post(self.url, post_data)
        self.assertEqual(response.status_code, 200)
        payment = Payment.objects.get(pin='555-666')
        self.assertTrue(payment.used)
