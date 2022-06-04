from flask import Blueprint

from controller.trade_api import trade_api
from error.invalid_account import InvalidAccountError
from util.result import Result

import traceback

trade_error = Blueprint("trade_error", __name__)
prefix = "10"


@trade_api.errorhandler(InvalidAccountError)
def invalid_account_error(error):
    return Result.error(prefix + "1", "账号密码错误")

@trade_api.errorhandler(Exception)
def unknown_error(error):
    traceback.print_exc()
    return Result.error(prefix + "0", "未知错误，请联系管理员")
