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

# 个人证券账户开户
@account_admin_api.route("/account_admin/add_personal_securities_account", methods=["POST"])
def add_personal_securities_account():
    data = json.loads(request.get_data(as_text=True))
    AccountAdminService.add_personal_securities_account(data)
    return Result.success(None)

# 法人证券账户开户
@account_admin_api.route("/account_admin/add_legal_person_securities_account", methods=["POST"])
def add_legal_person_securities_account():
    data = json.loads(request.get_data(as_text=True))
    AccountAdminService.add_legal_person_securities_account(data)
    return Result.success(None)

# 资金账户开户
@account_admin_api.route("/account_admin/add_fund_account", methods=["POST"])
def add_fund_account():
    data = json.loads(request.get_data(as_text=True))
    AccountAdminService.add_fund_account(data)
    return Result.success(None)

# 资金账户存取款
@account_admin_api.route("/account_admin/modify_money", methods=["POST"])
def modify_money():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    AccountAdminService.modify_money(data)
    return Result.success(None)

# 资金账户修改密码
@account_admin_api.route("/account_admin/fund_change_password", methods=["POST"])
def fund_change_password():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    AccountAdminService.fund_change_password(data)
    return Result.success(None)

# 资金账户销户
@account_admin_api.route("/account_admin/fund_delete", methods=["POST"])
def fund_delete():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    AccountAdminService.fund_delete(data)
    return Result.success(None)

# 个人证券账户冻结
@account_admin_api.route("/account_admin/personal_security_freeze", methods=["POST"])
def personnal_security_freeze():
    data = json.loads(request.get_data(as_text=True))
    AccountAdminService.personal_security_freeze(data)
    return Result.success(None)

# 法人证券账户冻结
@account_admin_api.route("/account_admin/legal_person_security_freeze", methods=["POST"])
def legal_person_security_freeze():
    data = json.loads(request.get_data(as_text=True))
    AccountAdminService.legal_person_security_freeze(data)
    return Result.success(None)

# 资金账户冻结
@account_admin_api.route("/account_admin/fund_freeze", methods=["POST"])
def fund_freeze():
    data = json.loads(request.get_data(as_text=True))
    AccountAdminService.fund_freeze(data)
    return Result.success(None)