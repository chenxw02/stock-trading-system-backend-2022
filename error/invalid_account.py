class InvalidAccountError(Exception):
    pass


class NoneAccountError(Exception):
    pass


class FrozenAccountError(Exception):
    pass


class ConditionNotMeetError(Exception):
    pass


class NoSecuritiesError(Exception):
    pass


class MulOpenAccountError(Exception):
    pass


class WithFundAccountError(Exception):
    pass


class MulSecuritiesAccountError(Exception):
    pass
