import jwt
import json
from flask import Blueprint, request
from service.query_user_service import QueryUserService
from util.result import Result
from config import jwt_secret_key
from error.query_user_error import MissAccountError,NotSamePasswordError
query_user_api = Blueprint('query_user_api', __name__)


@query_user_api.route("/query_user/login", methods=["POST"])
def query_user_login():
    data = json.loads(request.get_data(as_text=True))
    get_name = data.get("ID")
    get_psw = data.get("password")
    if not all([get_name, get_psw]):
            raise MissAccountError()
    token = QueryUserService.login(data["ID"], data["password"])
    authority = token.get("type")
    ID = token.get("query_user_id")
    info = {
        "type": authority,
        "user_id": ID
    }
    return Result.success(info)


@query_user_api.route("/query_user/register", methods=["POST"])
def query_user_register():
    data = json.loads(request.get_data(as_text=True))
    QueryUserService.register(data)
    return Result.success(None)

@query_user_api.route("/query_user/modify", methods=["POST"])
def query_user_modify():
    data = json.loads(request.get_data(as_text=True))
    #  首先要检查登陆状态然后在跳转到此界面
    #  这个界面的输入 用户ID 密码 确认密码
    #  ID password re_password
    get_password = data.get("password")
    get_re_password = data.get("re_password")
    if get_password != get_re_password:
        raise NotSamePasswordError()
    QueryUserService.modify(data)
    return Result.success(None)

@query_user_api.route("/query_user/upgrade", methods=["POST"])
def query_user_upgrade():
    data = json.loads(request.get_data(as_text=True))
    QueryUserService.upgrade(data)
    return Result.success(None)


if __name__ == '__main__':
    query_user_api.run()