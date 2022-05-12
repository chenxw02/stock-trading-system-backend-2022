import json

from flask import Blueprint, request

import admin_service

admin_api = Blueprint('admin_api', __name__)

@admin_api.route("/admin/login", methods=["POST"])
def login():
    data = json.loads(request.get_data(as_text=True))
    token = admin_service.login(data["admin_id"], data["password"])
    return token