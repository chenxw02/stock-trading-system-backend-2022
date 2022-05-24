import json
from flask import Blueprint, request
from service.admin_service import AdminService
from result import Result

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
