import json
from flask import Blueprint, request
from service.trans_res_service import AggAucService
from util.result import Result

trans_res_api = Blueprint('trans_res_api', __name__)

@trans_res_api.route("/trans_res", methods=["POST"])
def register():
    instruction_id = json.loads(request.get_data(as_text=True))
    # print(data)
    TransResService.register(instruction_id)
    return Result.success(None)