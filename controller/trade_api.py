# coding:utf-8
import json
from flask import Blueprint, request
from service.trade_service import TradeService
from util.result import Result
from util.auth import decode_token
import time

trade_api = Blueprint('trade_api', __name__)


@trade_api.route("/trade/login", methods=["POST"])
def login():
    data = json.loads(request.get_data(as_text=True))
    token = TradeService.login(data["user_id"], data["password"])
    return Result.success(token)


@trade_api.route("/trade/getMaxAmount", methods=["POST"])
def get_max_amount():
    token = request.headers.get('Authorization')
    info = decode_token(token)
    uID = info["user_id"]
    data = json.loads(request.get_data(as_text=True))
    print(data)
    res = TradeService.get_max_amount(data["stock_ID"], data["tType"], uID, data["price"])
    if res is None or res == 1:
        return Result.error(1, "max stock amount calculation error")
    print(res)

    return Result.success(res)


@trade_api.route("/trade/getMinMax", methods=["POST"])
def get_price_range():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    res = TradeService.get_price_range(data["stock_ID"])
    print(res)
    if res is None:
        return Result.error(1, "No stock with this ID!")

    return Result.success(res)


@trade_api.route("/trade/checkTransaction", methods=["POST"])
def check_transaction():
    token = request.headers.get('Authorization')
    info = decode_token(token)
    uID = info["user_id"]
    data = json.loads(request.get_data(as_text=True))
    print(data)
    amount = int(data["amount"])
    res = TradeService.check_transaction(data["stock_ID"], data["tType"], data['price'], amount, uID)
    print(res)

    if res == 0:
        TradeService.create_instruction(data["stock_ID"], data["tType"], data['price'], amount, data['uID'])
        TradeService.freeze_assets(data["stock_ID"], data["tType"], data['price'], amount, data['uID'])

        return Result.success(res)

    elif res == 1:
        return Result.error(1, "没有这只股票！")
    elif res == 2:
        return Result.error(2, "该股票暂时无法交易！")
    elif res == 3:
        return Result.error(3, "价格不能低于跌停板价格！")
    elif res == 4:
        return Result.error(4, "价格不能高于涨停板价格！")
    elif res == 5:
        return Result.error(5, "您的可用资金不足！")
    elif res == 6:
        return Result.error(6, "您没有这只股票的持仓！")
    elif res == 7:
        return Result.error(7, "您当前可用股票数量不足")
    elif res == 8:
        return Result.error(8, "委托数量不能为0！")
    elif res == 9:
        return Result.error(9, "委托数量只能是100的整数倍！")
    elif res == 10:
        return Result.error(10, "当前非交易时间段！")


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
    res = TradeService.update(data["stock_id"], data["fund_account_number"], data["buy_sell_flag"],
                              data["transaction_amount"], data["transaction_number"])
    return Result.success(res)


@trade_api.route("/stock/info", methods=["POST"])
def stock_info():
    stock_id = request.headers.get('stock_id')
    res = TradeService.show_stock_info(stock_id)
    if (res == 1):
        return Result.error(1, "没有这只股票！")
    else:
        return Result.success(res)


@trade_api.route("/instruction/info", methods=["GET"])
def instruction_info():
    token = request.headers.get('Authorization')
    info = decode_token(token)
    fund_acc_num = info["user_id"]
    res = TradeService.show_instruction_info(fund_acc_num)
    return Result.success(res)