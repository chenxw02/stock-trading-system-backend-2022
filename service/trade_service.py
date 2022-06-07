#coding:utf-8
import jwt
import bcrypt
import time
from config import jwt_secret_key
from dao.trade_dao import TradeDao
from error.invalid_account import InvalidAccountError
from error.invalid_jwt import InvalidJWT
import datetime

class TradeService:
    @staticmethod
    def login(user_id, password):
        user = TradeDao.get(user_id)
        print(user)
        if user is None:
            raise InvalidAccountError()
        encrypted_password = user.login_password
        print(encrypted_password, password)
       
        if not bcrypt.checkpw(password.encode("utf-8"), encrypted_password.encode("utf-8")):
            raise InvalidAccountError()
            
        headers = {
            "alg": "HS256",
            "typ": "JWT"
        }
        # 设置超时时间：当前时间的30分钟以后超时
        exp = int(time.time() + 60*30)
        payload = {
            "user_id": user_id,
            "type": "user",
            "exp": exp
        }
        token = jwt.encode(payload=payload, key=jwt_secret_key, algorithm='HS256', headers=headers)
        return token
    
    @staticmethod
    def get_max_amount(sID, tType, uID, price):
        price = float(price)

        stock_data = TradeDao.get_stock(sID)
        if stock_data is None:
            return None

        if tType == "buy":
            funds_data = TradeDao.get_user_funds(uID)
            balance = funds_data["balance"]-funds_data["frozen"]-funds_data["taken"]
            res = int(int(balance / (price*100)))*100
            # if(res<100):
            #     res=0
            # else:
            #     res=int(int(balance / price))
        else:
            user_stock = TradeDao.get_user_stock(uID, sID)
            if user_stock is None:
                return 1
            stock_own_count = user_stock["own"] - user_stock["frozen"]
            print(stock_own_count)
            res = stock_own_count
        return res

    @staticmethod
    def get_price_range(sID):
        stock_data = TradeDao.get_stock(sID)
        if stock_data is None:
            return None

        k_data = TradeDao.get_K_endprice(sID) #get last days k data
        if k_data is None:
            return None

        max_price = k_data["endprice"] + (k_data["endprice"] * stock_data["up"]/100)
        min_price = k_data["endprice"] - (k_data["endprice"] * stock_data["down"]/100)
    
        return (max_price, min_price)

    @staticmethod
    def freeze_assets(sID, tType, price, amount, uID):
        price = float(price)
        amount = int(amount)

        if tType == 'buy':
            total_price = price * amount
            TradeDao.freeze_funds(uID, total_price)

        else:
            TradeDao.freeze_stock(sID, uID, amount)

    @staticmethod
    def create_instruction(sID, tType, price, amount, uID):
        price = float(price)
        amount = int(amount)


        new_tID = TradeDao.get_latest_instruction_ID()
        if new_tID is None:
            new_tID = 0

        new_tID = int(int(new_tID) + 1)

        print(new_tID)
        time = str(datetime.datetime.now().strftime("%d%H%M%S"))
        print(time)




        if tType == 'buy':
            tType = 'B'
        else:
            tType = 'S'

        TradeDao.create_instruction(sID, tType, price, amount, uID, new_tID, time)

        return new_tID


    @staticmethod
    def check_transaction(sID, tType, price, amount, uID):
        price = float(price)
        amount = int(amount)
        timenow = int(datetime.datetime.now().strftime('%H%M%S'))

        stock_data = TradeDao.get_stock(sID)  #gets stock information
        if stock_data is None:
            return 1    # if no stock was found (no stock with sID)

        print(stock_data)
        if stock_data["status"] == 'F':
            return 2   #if stockID exists, but said stock is untradeable

        k_data = TradeDao.get_K_endprice(sID) #get last days k data
        print(k_data)

        # calculate the minimum price according to up&downs
        
        max_price = k_data["endprice"] + (k_data["endprice"] * stock_data["up"]/100)
        min_price = k_data["endprice"] - (k_data["endprice"] * stock_data["down"]/100 )
       
        print(max_price, min_price)
        if price < min_price:
            return 3    #if the buying price is too low
        elif price > max_price:
            return 4    #if the buying price is too high
        elif amount==0:
            return 8
        elif amount%100!=0:
            return 9
        elif timenow < 0 or (timenow >113000 and timenow<130000) or timenow>240000:
            return 10


        if tType == 'buy':
            funds = TradeDao.get_user_funds(uID)
            available = funds['balance'] - funds['frozen'] - funds['taken']
            total_price = price * amount
            if available < total_price:  # if the user does not have enough funds for the transaction
                return 5

        else:
            user_stock = TradeDao.get_user_stock(uID, sID)
            if user_stock is None:
                return 6                  #if the user wants to sell a stock he does not hold
            stock_own_count = user_stock["own"] - user_stock["frozen"]

            if stock_own_count < amount:  # if the user does not have enough stock for the transaction
                return 7


        #flag = TradeDao.check_min_price(sID,price)

        #flag = TradeDao.check_transaction(sID, tType, price, amount, uID)

        #if flag == 0:
           # TradeDao.create_instruction(sID, tType, price, amount, uID)
            #TradeDao.freeze_assets(sID, tType, price, amount, uID)

        return 0
        
    @staticmethod
    def show_fund_info(fund_acc_num):
        data = TradeDao.get_fund_info(fund_acc_num)
        # if data is None:
        #     raise
        return data
    
    @staticmethod
    def show_own_stock_info(fund_acc_num):
        data = TradeDao.get_own_stock_info(fund_acc_num)
        # if data is None:
        #     raise
        return data

    @staticmethod
    def update(stock_id, fund_acc_num, buy_sell_flag, amount, num, ins_id):
        #账户和flag对调
        data = TradeDao.update(stock_id, fund_acc_num, buy_sell_flag, amount, num, ins_id)
        return data
   
    @staticmethod
    def show_stock_info(stock_id):
        data = TradeDao.get_stock_info(stock_id)
        if data is None:
            return 1
        else:
            return data
    
    @staticmethod
    def show_instruction_info(fund_acc_num):
        data = TradeDao.get_instruction_info(fund_acc_num)
        # if data is None:
        #     raise
        return data
    
    @staticmethod
    def do_withdraw(fund_acc_num, keys):
        data = TradeDao.do_do_withdraw(fund_acc_num, keys)
        # if data is None:
        #     raise
        return data
    