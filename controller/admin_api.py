import json
from flask import Blueprint, request
from service.admin_service import AdminService
from util.result import Result
from util.auth import decode_token
from error.invalid_jwt import InvalidJWT

admin_api = Blueprint('admin_api', __name__)


@admin_api.route("/admin/login", methods=["POST"])
def login():
    data = json.loads(request.get_data(as_text=True))
    token = AdminService.login(data["admin_id"], data["password"])
    return Result.success(token)


@admin_api.route("/admin", methods=["POST"])
def register():
    data = json.loads(request.get_data(as_text=True))
    # print(data)
    AdminService.register(data)
    return Result.success(None)


@admin_api.route("/admin", methods=["PUT"])
def change_password():
    data = json.loads(request.get_data(as_text=True))
    token = request.headers.get('Authorization')
    info = decode_token(token)
    admin_id = info["admin_id"]
    auth_type = info["type"]
    if auth_type != "admin":
        raise InvalidJWT
    AdminService.change_password(admin_id, data["password"], data["new_password"])
    return Result.success(None)

@admin_api.route("/admin/permission", methods=["GET"])
def get_permissions():
    token = request.headers.get('Authorization')
    info = decode_token(token)
    admin_id = info["admin_id"]
    auth_type = info["type"]
    if auth_type != "admin":
        raise InvalidJWT
    stocks = AdminService.get_permissions(admin_id)
    return Result.success(stocks)

@admin_api.route("/admin/stock_status", methods=["PUT"])
def set_status():
    data = json.loads(request.get_data(as_text=True))
    token = request.headers.get('Authorization')
    info = decode_token(token)
    admin_id = info["admin_id"]
    auth_type = info["type"]
    if auth_type != "admin":
        raise InvalidJWT
    AdminService.set_status(data["stock_id"], data["stock_status"])
    return Result.success(None)
