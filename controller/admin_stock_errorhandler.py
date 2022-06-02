from flask import Blueprint

from controller.admin_stock_api import admin_stock_api
from error.invalid_jwt import InvalidJWT
from util.result import Result

import traceback

admin_stock_error = Blueprint("admin_stock_error", __name__)
prefix = "10"


@admin_stock_api.errorhandler(InvalidJWT)
def invalid_jwt_error(error):
    return Result.error(prefix + "1", "请重新登陆")


@admin_stock_api.errorhandler(Exception)
def unknown_error(error):
    traceback.print_exc()
    return Result.error(prefix + "0", "未知错误，请联系管理员")
