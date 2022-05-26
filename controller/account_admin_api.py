import json
from flask import Blueprint, request
from service.account_admin_service import AccountAdminService
from util.result import Result

account_admin_api = Blueprint('account_admin_api', __name__)


@account_admin_api.route("/account_admin/login", methods=["POST"])
def login():
    data = json.loads(request.get_data(as_text=True))
    token = AccountAdminService.login(data["administrator_id"], data["administrator_password"])
    return Result.success(token)


@account_admin_api.route("/account_admin", methods=["POST"])
def register():
    data = json.loads(request.get_data(as_text=True))
    # print(data)
    AccountAdminService.register(data)
    return Result.success(None)
