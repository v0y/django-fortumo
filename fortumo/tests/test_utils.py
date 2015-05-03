from django.test import TestCase
from mock import patch


from fortumo import consts
from fortumo.models import Service, Payment, Message
from fortumo.utils import (
    calculate_signature,
    generate_pin,
    generate_unique_pin,
    signature_is_valid,
)


class SignatureTestCase(TestCase):

    def setUp(self):
        self.data = {
            'credit_name': 'gold',
            'tc_amount': '3333',
            'tc_id': '291',
            'test': 'ok',
            'sig': '047f555536f8826825c9079265ad36de',
        }

    def test_calculate_signature(self):
        self.assertEqual(calculate_signature(self.data), self.data['sig'])

    def test_valid_signature_is_valid(self):
        self.assertTrue(signature_is_valid(self.data))

    def test_invalid_signature_is_invalid(self):
        self.data['credit_name'] = 'silver'
        self.assertFalse(signature_is_valid(self.data))


class PinTestCase(TestCase):
    _pin_generations_count = 0

    def _mock_generate_pin(*args, **kwargs):
        if PinTestCase._pin_generations_count == 0:
            PinTestCase._pin_generations_count += 1
            return '111-111'
        else:
            return '222-222'

    def test_generate_pin(self):
        pin = generate_pin()
        part1, part2 = pin.split('-')
        self.assertEqual(type(pin), str)
        self.assertEqual(len(pin), 7)
        self.assertEqual(len(part1), 3)
        self.assertEqual(len(part2), 3)
        self.assertTrue(0 <= int(part1) <= 999)
        self.assertTrue(0 <= int(part2) <= 999)

    @patch('fortumo.utils.generate_pin', _mock_generate_pin)
    def test_generate_uniqie_pin(self):
        service_id = 'f7fa12b381d290e268f99e382578d64a'
        service = Service.objects.create(
            service_id=service_id,
            secret='123',
        )
        message_data = {
            'message': '123',
            'sender': '358401234567',
            'country': 'SE',
            'price': 0.32,
            'price_wo_vat': 0.27,
            'currency': 'SEK',
            'service_id': service_id,
            'message_id': '123456',
            'keyword': 'KEY',
            'shortcode': 1311,
            'operator': 'Vodafone',
            'billing_type': consts.BillingType.MO,
            'status': consts.Status.OK,
            'test': consts.Test.FALSE,
            'sig': '8d5714783f9cb60aa5798f892bbf3baf',
        }
        message1 = Message.objects.create(**message_data)
        message2 = Message.objects.create(**message_data)
        Payment.objects.create(
            service=service,
            pin='111-111',
            used=False,
            message=message1,
        )
        Payment.objects.create(
            service=service,
            pin='222-222',
            used=True,
            message=message2,
        )
        self.assertEqual(generate_unique_pin(service_id), '222-222')
