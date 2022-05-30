import json
from flask import Blueprint, request
from service.con_auc_main import ConAucService
from util.result import Result

con_auc_api = Blueprint('con_auc_api', __name__)

# @admin_api.route("/admin/login", methods=["POST"])
# def login():
#     data = json.loads(request.get_data(as_text=True))
#     token = AdminService.login(data["admin_id"], data["password"])
#     return Result.success(token)

@con_auc_api.route("/con_auc", methods=["POST"])
def con_auc():
    data = json.loads(request.get_data(as_text=True))
    # print(data)
    instruction_id = data.get("instruction_id")
    ConAucService.con_auc(instruction_id)
    return Result.success(None)