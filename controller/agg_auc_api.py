import json
from flask import Blueprint, request
from service.agg_auc_service import AggAucService
from result import Result

agg_auc_api = Blueprint('agg_auc_api', __name__)

@agg_auc_api.route("/agg_auc", methods=["POST"])
def register():
    instruction_id = json.loads(request.get_data(as_text=True))
    # print(data)
    AggAucService.register(instruction_id)
    return Result.success(None)