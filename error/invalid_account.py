class InvalidAccountError(Exception):
    pass

class InvalidAccountNameError(Exception):
    pass

class MissAccountError(Exception):
    pass

class NotSamePasswordError(Exception):
    pass

class NoneAccountNameError(Exception):
    pass

class InvalidPaymentAccountError(Exception):
    pass

class LackOfBalance(Exception):
    pass

class AlreadyAdvance(Exception):
    pass