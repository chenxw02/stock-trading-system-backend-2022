from flask import Blueprint

from controller.account_admin_api import account_admin_api
from error.invalid_account import InvalidAccountError
from util.result import Result

account_admin_error = Blueprint("account_admin_error", __name__)
prefix = "10"


@account_admin_api.errorhandler(InvalidAccountError)
def invalid_account_error(error):
    return Result.error(prefix+"1", "账号密码错误")


@account_admin_api.errorhandler(Exception)
def invalid_account_error(error):
    return Result.error(prefix+"0", "未知错误，请联系管理员")