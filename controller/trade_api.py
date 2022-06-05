import json
from flask import Blueprint, request
from service.trade_service import TradeService
from util.result import Result
from util.auth import decode_token

trade_api = Blueprint('trade_api', __name__)

@trade_api.route("/trade/login", methods=["POST"])
def login():
    data = json.loads(request.get_data(as_text=True))
    token = TradeService.login(data["user_id"], data["password"])
    return Result.success(token)

@trade_api.route("/trade/checkTransaction", methods=["POST"])
def check_transaction():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    res = TradeService.check_transaction(data["stock_ID"], data["tType"], data['price'], data['amount'], data['uID'])
    if res == 0:
        return Result.success(res)
    elif res == 1:
        return Result.error(1, "No stock with this ID!")
    elif res == 2:
        return Result.error(2, "This stock is not Tradeable!")
    elif res == 3:
        return Result.error(3, "The buying price is too low!")
    elif res == 4:
        return Result.error(4, "Not enough funds!")
    elif res == 5:
        return Result.error(5, "Not enough stock!")

@trade_api.route("/fund/info", methods=["GET"])
def fund_info():
    token = request.headers.get('Authorization')
    info = decode_token(token)
    fund_acc_num = info["user_id"]
    res = TradeService.show_fund_info(fund_acc_num)
    return Result.success(res)

@trade_api.route("/ownstock/info", methods=["GET"])
def own_stock_info():
    token = request.headers.get('Authorization')
    info = decode_token(token)
    fund_acc_num = info["user_id"]
    res = TradeService.show_own_stock_info(fund_acc_num)
    return Result.success(res)

@trade_api.route("/transaction/update", methods=["POST"])
def update():
    data = json.loads(request.get_data(as_text=True))
    res = TradeService.update(data["stock_id"], data["fund_account_number"], data["buy_sell_flag"], data["transaction_amount"], data["transaction_number"])
    return Result.success(res)