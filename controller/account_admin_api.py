import json
from flask import Blueprint, request
from service.account_admin_service import AccountAdminService
from util.result import Result

account_admin_api = Blueprint('account_admin_api', __name__)


# 管理员登录
@account_admin_api.route("/account_admin/login", methods=["POST"])
def login():
    data = json.loads(request.get_data(as_text=True))
    # print(data)
    token = AccountAdminService.login(data["administrator_id"], data["administrator_password"])
    return Result.success(token)


# 管理员注册（前端无此接口，测试用）
@account_admin_api.route("/account_admin/register", methods=["POST"])
def register():
    data = json.loads(request.get_data(as_text=True))
    # print(data)
    AccountAdminService.register(data)
    return Result.success(None)


# 展示所有的要审批的指令
@account_admin_api.route("/account_admin/show_deal", methods=["POST"])
def show_deal():
    return Result.success(AccountAdminService.show_deal())


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


# 个人证券账户解冻
@account_admin_api.route("/account_admin/personal_security_thaw", methods=["POST"])
def personal_security_thaw():
    data = json.loads(request.get_data(as_text=True))
    AccountAdminService.personal_security_thaw(data)
    return Result.success(None)


# 法人证券账户冻结
@account_admin_api.route("/account_admin/legal_person_security_freeze", methods=["POST"])
def legal_person_security_freeze():
    data = json.loads(request.get_data(as_text=True))
    AccountAdminService.legal_person_security_freeze(data)
    return Result.success(None)


# 法人证券账户解冻
@account_admin_api.route("/account_admin/legal_person_security_thaw", methods=["POST"])
def legal_person_security_thaw():
    data = json.loads(request.get_data(as_text=True))
    AccountAdminService.legal_person_security_thaw(data)
    return Result.success(None)


# 资金账户冻结
@account_admin_api.route("/account_admin/fund_freeze", methods=["POST"])
def fund_freeze():
    data = json.loads(request.get_data(as_text=True))
    AccountAdminService.fund_freeze(data)
    return Result.success(None)


# 资金账户解冻
@account_admin_api.route("/account_admin/fund_thaw", methods=["POST"])
def fund_thaw():
    data = json.loads(request.get_data(as_text=True))
    AccountAdminService.fund_thaw(data)
    return Result.success(None)


# 重新开户（个人证券账户）
@account_admin_api.route("/account_admin/re_add_personal_securities_account", methods=["POST"])
def re_add_personal_securities_account():
    data = json.loads(request.get_data(as_text=True))
    AccountAdminService.re_add_personal_securities_account(data)
    return Result.success(None)


# 重新开户（法人证券账户）
@account_admin_api.route("/account_admin/re_add_legal_person_securities_account", methods=["POST"])
def re_add_legal_person_securities_account():
    data = json.loads(request.get_data(as_text=True))
    AccountAdminService.re_add_legal_person_securities_account(data)
    return Result.success(None)


# 证券账户销户
@account_admin_api.route("/account_admin/securities_account_delete", methods=["POST"])
def securities_account_delete():
    data = json.loads(request.get_data(as_text=True))
    AccountAdminService.securities_account_delete(data)
    return Result.success(None)


# 按查询条件返回所有证券账户信息
@account_admin_api.route("/account_admin/get_securities_account_information_by_query", methods=["POST"])
def get_securities_account_information_by_query():
    data = json.loads(request.get_data(as_text=True))
    return Result.success(AccountAdminService.get_securities_account_information_by_query(data))


# 按查询条件返回所有资金账户信息
@account_admin_api.route("/account_admin/get_fund_account_information_by_query", methods=["POST"])
def get_fund_account_information_by_query():
    data = json.loads(request.get_data(as_text=True))
    return Result.success(AccountAdminService.get_fund_account_information_by_query(data))


# 重新开户（资金账户）
@account_admin_api.route("/account_admin/re_add_fund_account", methods=["POST"])
def re_add_fund_account():
    data = json.loads(request.get_data(as_text=True))
    AccountAdminService.re_add_fund_account(data)
    return Result.success(None)