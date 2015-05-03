from fortumo.utils import (
    calculate_signature,
    generate_pin,
    signature_is_valid,
)


def test_calculate_signature():
    data = {
        'credit_name': 'gold',
        'tc_amount': '3333',
        'tc_id': '291',
        'test': 'ok',
        'sig': '047f555536f8826825c9079265ad36de',
    }
    signature = calculate_signature(data)
    expected_signature = '047f555536f8826825c9079265ad36de'

    assert signature == expected_signature


def test_valid_signature_is_valid():
    data = {
        'credit_name': 'gold',
        'tc_amount': '3333',
        'tc_id': '291',
        'test': 'ok',
        'sig': '047f555536f8826825c9079265ad36de',
    }
    assert signature_is_valid(data) is True


def test_invalid_signature_is_invalid():
    data = {
        'credit_name': 'silver',
        'tc_amount': '3333',
        'tc_id': '291',
        'test': 'ok',
        'sig': '047f555536f8826825c9079265ad36de',
    }
    assert signature_is_valid(data) is False


def test_generate_pin():
    pin = generate_pin()
    part1, part2 = pin.split('-')
    assert type(pin) == str
    assert len(pin) == 7
    assert len(part1) == 3
    assert len(part2) == 3
    assert 0 <= int(part1) <= 999
    assert 0 <= int(part2) <= 999