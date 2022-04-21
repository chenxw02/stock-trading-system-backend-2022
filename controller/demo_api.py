from flask import Blueprint

demo_api = Blueprint('demo_api', __name__)


@demo_api.route("/demo", methods=["GET"])
def demo_get():
    return 'get-stock-trading-system-backend'


@demo_api.route("/demo", methods=["POST"])
def demo_post():
    return 'post-stock-trading-system-backend'
