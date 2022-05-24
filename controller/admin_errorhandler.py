from flask import Blueprint

from admin_api import admin_api
from error.invalid_account import InvalidAccountError
from result import Result

admin_error = Blueprint("admin_error", __name__)
prefix = "10"

@admin_api.errorhandler(InvalidAccountError)
def invalid_account_error(error):
    return Result.error(prefix+"1", "账号密码错误")

@admin_api.errorhandler(Exception)
def invalid_account_error(error):
    return Result.error(prefix+"0", "未知错误，请联系管理员")