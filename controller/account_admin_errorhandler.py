from flask import Blueprint

from controller.account_admin_api import account_admin_api
from error.invalid_account import InvalidAccountError
from error.invalid_account import NoneAccountError
from error.invalid_account import FrozenAccountError
from error.invalid_account import ConditionNotMeetError
from error.invalid_account import NoSecuritiesError
from error.invalid_account import MulOpenAccountError
from error.invalid_account import WithFundAccountError
from error.invalid_account import MulSecuritiesAccountError
from error.wrong_money import MinusMoneyError
from error.wrong_money import NoMoneyError
from error.wrong_money import RemainMoneyError
from util.result import Result

account_admin_error = Blueprint("account_admin_error", __name__)
prefix = "10"


@account_admin_api.errorhandler(InvalidAccountError)
def invalid_account_error(error):
    return Result.error(prefix + "1", "账号密码错误")


@account_admin_api.errorhandler(NoneAccountError)
def invalid_account_error(error):
    return Result.error(prefix + "1", "未找到账户")


@account_admin_api.errorhandler(FrozenAccountError)
def invalid_account_error(error):
    return Result.error(prefix + "1", "该账户已冻结")


@account_admin_api.errorhandler(Exception)
def invalid_account_error(error):
    return Result.error(prefix + "0", "未知错误，请联系管理员")


@account_admin_api.errorhandler(MinusMoneyError)
def wrong_money_error(error):
    return Result.error(prefix + "1", "金额不能为负数")


@account_admin_api.errorhandler(NoMoneyError)
def wrong_money_error(error):
    return Result.error(prefix + "1", "资金不足")


@account_admin_api.errorhandler(RemainMoneyError)
def wrong_money_error(error):
    return Result.error(prefix + "1", "该资金账户尚有存款")


@account_admin_api.errorhandler(ConditionNotMeetError)
def condition_not_meet_error(error):
    return Result.error(prefix + "1", "该账户不满足重新开户条件")


@account_admin_api.errorhandler(NoSecuritiesError)
def no_securities_error(error):
    return Result.error(prefix + "1", "对应证券账户不存在")


@account_admin_api.errorhandler(MulOpenAccountError)
def invalid_account_error(error):
    return Result.error(prefix + "1", "您已开过账户，请勿重复开设")


@account_admin_api.errorhandler(WithFundAccountError)
def with_fund_account_error(error):
    return Result.error(prefix + "1", "证券账户下还有资金账户！")


@account_admin_api.errorhandler(MulSecuritiesAccountError)
def mul_securities_account_error(error):
    return Result.error(prefix + "1", "该证券账户已开过资金账户！")