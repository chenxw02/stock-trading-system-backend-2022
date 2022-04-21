from flask import Blueprint

admin_api = Blueprint('admin_api', __name__)


@admin_api.route("/admin", methods=["GET"])
def demo_get():
    return 'get-stock-trading-system-backend'


@admin_api.route("/admin", methods=["POST"])
def demo_post():
    return 'post-stock-trading-system-backend'