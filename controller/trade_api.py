import json
from flask import Blueprint, request
from service.trade_service import TradeService
from util.result import Result

trade_api = Blueprint('trade_api', __name__)

@trade_api.route("/fund/info", methods=["POST"])
def fund_info():
    data = json.loads(request.get_data(as_text=True))
    res = TradeService.show_fund_info(data["fund_account_number"])
    return Result.success(res)

@trade_api.route("/ownstock/info", methods=["POST"])
def own_stock_info():
    data = json.loads(request.get_data(as_text=True))
    res = TradeService.show_own_stock_info(data["fund_account_number"])
    return Result.success(res)

@trade_api.route("/update/buy", methods=["POST"])
def update_buy():
    data = json.loads(request.get_data(as_text=True))
    res = TradeService.update_buy(data["transaction_id"])
    return Result.success(res)

@trade_api.route("/update/sell", methods=["POST"])
def update_sell():
    data = json.loads(request.get_data(as_text=True))
    res = TradeService.update_sell(data["transaction_id"])
    return Result.success(res)