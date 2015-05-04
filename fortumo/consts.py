class Status(object):
    OK = 'ok'
    PENDING = 'pending'
    FAILED = 'failed'


class Test(object):
    OK = 'ok'
    FALSE = 'false'


class BillingType(object):
    MO = 'MO'
    MT = 'MT'


class PinResponse(object):
    VALID = 'ok'
    INVALID = 'invalid'
