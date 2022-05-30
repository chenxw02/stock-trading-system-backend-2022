import json
from flask import Blueprint, request
from service.agg_auc_main import AggAucService
from util.result import Result

agg_auc_api = Blueprint('agg_auc_api', __name__)

# @admin_api.route("/admin/login", methods=["POST"])
# def login():
#     data = json.loads(request.get_data(as_text=True))
#     token = AdminService.login(data["admin_id"], data["password"])
#     return Result.success(token)

@agg_auc_api.route("/agg_auc", methods=["POST"])
def agg_auc():
    instruction_id = json.loads(request.get_data(as_text=True))
    # print(data)
    AggAucService.agg_auc(instruction_id)
    return Result.success(None)