from flask import Blueprint

from controller.query_user_api import query_user_api
from error.query_user_error import InvalidAccountError,InvalidAccountNameError,MissAccountError,NotSamePasswordError,NoneAccountNameError,InvalidPaymentAccountError,LackOfBalance,AlreadyAdvance
from util.result import Result
query_user_error = Blueprint("query_user_error", __name__)
prefix = "40"

@query_user_api.errorhandler(InvalidAccountError)
def invalid_account_error(error):
    return Result.error(prefix+"1", "账号或密码错误")

@query_user_api.errorhandler(Exception)
def invalid_account_error(error):
    return Result.error(prefix+"0", "未知错误，请联系管理员")

@query_user_api.errorhandler(InvalidAccountNameError)
def invalid_account_error(error):
    return Result.error(prefix+"3", "该用户名已经存在")

@query_user_api.errorhandler(MissAccountError)
def invalid_account_error(error):
    return Result.error(prefix+"2", "请填写用户名或密码")

@query_user_api.errorhandler(NotSamePasswordError)
def invalid_account_error(error):
    return Result.error(prefix+"4", "两次填写的密码不一致")

@query_user_api.errorhandler(NoneAccountNameError)
def invalid_account_error(error):
    return Result.error(prefix+"5", "账户不存在，请重新输入")

@query_user_api.errorhandler(InvalidPaymentAccountError)
def InvalidPaymentAccountError(error):
    return Result.error(prefix+"6", "支付账户或支付密码错误")

@query_user_api.errorhandler(LackOfBalance)
def LackOfBalance(error):
    return Result.error(prefix+"8", "余额不足")


@query_user_api.errorhandler(AlreadyAdvance)
def AlreadyAdvance(error):
    return Result.error(prefix+"7", "该账户已经为高级账户")