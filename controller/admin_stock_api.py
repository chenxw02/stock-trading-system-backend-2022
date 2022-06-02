import json
from flask import Blueprint, request
from service.admin_stock_service import AdminStockService
from util.result import Result
from util.auth import decode_token
from error.invalid_jwt import InvalidJWT

admin_stock_api = Blueprint('admin_stock_api', __name__)


@admin_stock_api.route("/admin/permission", methods=["GET"])
def get_permissions():
    token = request.headers.get('Authorization')
    info = decode_token(token)
    admin_id = info["admin_id"]
    auth_type = info["type"]
    if auth_type != "admin":
        raise InvalidJWT
    stocks = AdminStockService.get_permissions(admin_id)
    return Result.success(stocks)


@admin_stock_api.route("/admin/stock_status", methods=["PUT"])
def set_status():
    data = json.loads(request.get_data(as_text=True))
    token = request.headers.get('Authorization')
    info = decode_token(token)
    admin_id = info["admin_id"]
    auth_type = info["type"]
    if auth_type != "admin":
        raise InvalidJWT
    AdminStockService.set_status(data["stock_id"], data["stock_status"])
    return Result.success(None)


@admin_stock_api.route("/admin/stock_threshold", methods=["PUT"])
def set_threshold():
    data = json.loads(request.get_data(as_text=True))
    token = request.headers.get('Authorization')
    info = decode_token(token)
    admin_id = info["admin_id"]
    auth_type = info["type"]
    if auth_type != "admin":
        raise InvalidJWT
    AdminStockService.set_threshold(data["stock_id"], data["rise_threshold"], data["fall_threshold"])
    return Result.success(None)
