import json
from flask import Blueprint, request
from service.account_admin_service import AccountAdminService
from util.result import Result

account_admin_api = Blueprint('account_admin_api', __name__)


@account_admin_api.route("/account_admin/login", methods=["POST"])
def login():
    data = json.loads(request.get_data(as_text=True))
    # print(data)
    token = AccountAdminService.login(data["administrator_id"], data["administrator_password"])
    return Result.success(token)


@account_admin_api.route("/account_admin/register", methods=["POST"])
def register():
    data = json.loads(request.get_data(as_text=True))
    # print(data)
    AccountAdminService.register(data)
    return Result.success(None)


@account_admin_api.route("/account_admin/show_deal", methods=["POST"])
def show_deal():
    return AccountAdminService.show_deal()


@account_admin_api.route("/account_admin/add_personal_securities_account", methods=["POST"])
def add_personal_securities_account():
    data = json.loads(request.get_data(as_text=True))
    AccountAdminService.add_personal_securities_account(data)
    return Result.success(None)


@account_admin_api.route("/account_admin/add_legal_person_securities_account", methods=["POST"])
def add_legal_person_securities_account():
    data = json.loads(request.get_data(as_text=True))
    AccountAdminService.add_legal_person_securities_account(data)
    return Result.success(None)


@account_admin_api.route("/account_admin/add_fund_account", methods=["POST"])
def add_fund_account():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    AccountAdminService.add_fund_account(data)
    return Result.success(None)


