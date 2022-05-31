from flask import Blueprint

from controller.admin_api import admin_api
from error.invalid_account import InvalidAccountError
from error.invalid_jwt import InvalidJWT
from util.result import Result

import traceback

admin_error = Blueprint("admin_error", __name__)
prefix = "10"

@admin_api.errorhandler(InvalidAccountError)
def invalid_account_error(error):
    return Result.error(prefix+"1", "账号密码错误")

@admin_api.errorhandler(InvalidJWT)
def invalid_jwt_error(error):
    return Result.error(prefix+"2", "请重新登陆")

@admin_api.errorhandler(Exception)
def invalid_account_error(error):
    traceback.print_exc()
    return Result.error(prefix+"0", "未知错误，请联系管理员")