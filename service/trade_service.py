import jwt
import bcrypt
import time
from config import jwt_secret_key
from dao.trade_dao import TradeDao
from error.invalid_account import InvalidAccountError
from error.invalid_jwt import InvalidJWT


class TradeService:
    @staticmethod
    def login(user_id, password):
        user = TradeDao.get(user_id)
        if user is None:
            raise InvalidAccountError()
        encrypted_password = user.login_password
        if not bcrypt.checkpw(password.encode("utf-8"), encrypted_password.encode("utf-8")):
            raise InvalidAccountError()
        # raise 以返回账号密码错误
        headers = {
            "alg": "HS256",
            "typ": "JWT"
        }
        # 设置超时时间：当前时间的30分钟以后超时
        exp = int(time.time() + 60 * 30)
        payload = {
            "user_id": user_id,
            "type": "user",
            "exp": exp
        }
        token = jwt.encode(payload=payload, key=jwt_secret_key, algorithm='HS256', headers=headers)
        return token

    @staticmethod
    def check_transaction(sID, tType, price, amount, uID):
        flag = TradeDao.check_transaction(sID, tType, price, amount, uID)

        if flag == 0:
            TradeDao.create_instruction(sID, tType, price, amount, uID)
            TradeDao.freeze_assets(sID, tType, price, amount, uID)

        return flag

    @staticmethod
    def show_fund_info(fund_acc_num):
        data = TradeDao.get_fund_info(fund_acc_num)
        return data

    @staticmethod
    def show_own_stock_info(fund_acc_num):
        data = TradeDao.get_own_stock_info(fund_acc_num)
        return data

    @staticmethod
    def update(stock_id, fund_acc_num, buy_sell_flag, amount, num):
        data = TradeDao.update(stock_id, fund_acc_num, buy_sell_flag, amount, num)
        return data