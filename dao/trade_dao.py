#coding:utf-8
from calendar import month
from exts import db
from model.account_admin import FundAccount
from model.account_admin import OwnStock
from model.center_trade import Stock
from model.center_trade import Transaction
from model.center_trade import K
from model.center_trade import Instruction
from sqlalchemy import and_
from sqlalchemy import func
import datetime


class TradeDao:
    @staticmethod
    def get(user_id):
        user = FundAccount.query.get(user_id)
        return user

    @staticmethod
    def get_stock(sID):
        data = db.session.query(Stock.stock_id, Stock.stock_type, Stock.stock_status) \
            .filter(Stock.stock_id == sID).all()

        if len(data) == 0:
            return None

        res = {"ID": data[0][0], "type": data[0][1], "status": data[0][2]}
        return res

    @staticmethod
    def get_K_endprice(sID):
        data = db.session.query(K.k_id, K.stock_id, K.end_price, K.date) \
            .filter(and_(K.stock_id == sID, K.end_price.isnot(None))).order_by(K.date.desc()).first()

        if data is None or len(data) == 0:
            return None

        res = {"endprice": data[2], "date": data[3]}
        return res

    @staticmethod
    def get_user_funds(uID):
        data = db.session.query(FundAccount.balance, FundAccount.frozen, FundAccount.taken) \
            .filter(FundAccount.fund_account_number == uID).first()
        res = {"balance": data[0], "frozen": data[1], "taken": data[2]}
        return res

    @staticmethod
    def get_user_stock(uID, sID):
        data = db.session.query(OwnStock.own_number, OwnStock.frozen) \
            .filter(and_(OwnStock.stock_id == sID, OwnStock.securities_account_number == uID)).first()
        if data is None or len(data) == 0:
            return None
        res = {"own": data[0], "frozen": data[1]}
        return res

    @staticmethod
    def get_latest_instruction_ID():
        data = db.session.query(func.max(Instruction.instruction_id)).first()[0]
        return data

    @staticmethod
    def freeze_funds(uID, total_price):
        funds = FundAccount.query.filter(FundAccount.fund_account_number == uID).first()
        funds.frozen += total_price
        db.session.commit()

    @staticmethod
    def create_instruction(sID, tType, price, amount, uID, tID, time):
        newInstruction = Instruction()
        newInstruction.instruction_id = tID
        newInstruction.stock_id = sID
        newInstruction.fund_account_number = uID
        newInstruction.buy_sell_flag = tType
        newInstruction.target_number = amount
        newInstruction.actual_number = 0
        newInstruction.target_price = price
        newInstruction.total_amount = 0.0
        newInstruction.time = time
        newInstruction.instruction_state = 'N'
        db.session.add(newInstruction)
        db.session.commit()

    @staticmethod
    def freeze_stock(sID, uID, amount):
        stock_own = OwnStock.query.filter(
            and_(OwnStock.stock_id == sID, OwnStock.securities_account_number == uID)).first()
        stock_own.frozen += amount
        db.session.commit()

    @staticmethod
    def get_fund_info(fund_acc_num):
        data = db.session.query(FundAccount.balance, FundAccount.frozen, FundAccount.taken).filter(FundAccount.fund_account_number == fund_acc_num).all()
        # 获取当日日期
        now_date = int(datetime.datetime.now().strftime('%Y%m%d'))
        data2 = db.session.query(func.sum(Transaction.transaction_amount)).filter(and_(Transaction.transaction_date == now_date, Transaction.fund_account_number == fund_acc_num, Transaction.buy_sell_flag == 'S')).all()
        if data2[0][0] is None:
            data2 = 0
        else:
            data2 = data2[0][0]
        res = {"fund_account_number": fund_acc_num, "balance": data[0][0], "frozen": data[0][1], "taken": data[0][2], "sellamount": data2}
        return res

    @staticmethod
    def get_own_stock_info(fund_acc_num):
        # 查询证券账户号码
        data = db.session.query(FundAccount.securities_account_number).filter(FundAccount.fund_account_number == fund_acc_num).all()
        acc = data[0][0]
        data2 = db.session.query(OwnStock.own_number, OwnStock.frozen, OwnStock.own_amount, Stock.stock_name, Stock.stock_id, Stock.price).join(OwnStock, OwnStock.stock_id == Stock.stock_id).filter(OwnStock.securities_account_number == acc).order_by(Stock.stock_name).all()
        res = []
        content = {}
        # 生成需要返回的结果
        for i in data2:
            content = {"own_number": i[0], "frozen": i[1], "own_amount": i[2], "stock_name": i[3], "stock_id": i[4], "price": i[5]}
            res.append(content)
        return res


    @staticmethod
    def update(sid, fund_acc_num, buy_sell_flag, amount, num):
        # 查询证券账户号码
        sec = db.session.query(FundAccount.securities_account_number).filter(FundAccount.fund_account_number == fund_acc_num).all()[0][0]
        
        fund_acc = FundAccount.query.filter(FundAccount.fund_account_number == fund_acc_num).first()
        own_stock = OwnStock.query.filter(and_(OwnStock.securities_account_number == sec, OwnStock.stock_id == sid)).first()
        
        if buy_sell_flag == 'S': #卖
            fund_acc.taken -= amount
            fund_acc.frozen -= amount

            own_stock.own_number -= num
            own_stock.frozen -= num
            own_stock.own_amount -= amount
            if own_stock.own_number == 0: #股票已全部卖出
                db.session.delete(own_stock)
        else: #买
            fund_acc.taken += amount
            fund_acc.frozen -= amount

            if own_stock is None: #own_stock里没有该股票的记录
                data = OwnStock(stock_id=sid, securities_account_number=sec, own_number=num, frozen=0, own_amount=amount)
                db.session.add(data)
            else:
                own_stock.own_number += num
                own_stock.own_amount += amount
        db.session.commit()

    @staticmethod
    def get_stock_info(stock_id):
        data = db.session.query(Stock.stock_name, Stock.price ,Stock.stock_type, Stock.stock_status).filter(Stock.stock_id == stock_id).all()
        if len(data) == 0: 
            return None
        else: 
            # 获取当日日期
            now_date = int(datetime.datetime.now().strftime('%Y%m%d'))
            if(datetime.datetime.now().day<7):
                weekflag=now_date-76
            else:
                weekflag=now_date-6
            
            
            data2 = db.session.query(K.start_price, K.lowest_price, K.highest_price, K.trade_amount).filter(K.stock_id==stock_id and K.date==now_date).all()
            data3 = db.session.query(func.max(K.highest_price), func.min(K.lowest_price)).filter(K.stock_id==stock_id and K.date>=weekflag).one()
            data4 = db.session.query(func.max(K.highest_price), func.min(K.lowest_price)).filter(K.stock_id==stock_id and K.date>=now_date-29).one()
            data5=db.session.query(K.end_price) \
            .filter(and_(K.stock_id == stock_id, K.end_price.isnot(None))).order_by(K.date.desc()).first()
            print(data5)

            
            
            res = {"id": stock_id, "name": data[0][0], "price": data[0][1], "type":data[0][2], "state":data[0][3],"start": data2[0][0], "volume":data2[0][3], "Dlow": data2[0][1], "Dhigh": data2[0][2], "Wlow": data3[1], "Whigh": data3[0], "Mlow":data4[1], "Mhigh":data4[0], "end": data5[0]}
            print(res)
            return res
    
    @staticmethod
    def get_instruction_info(fund_acc_num):
        now_day = str(datetime.datetime.now().strftime('%d'))
        tempflag1=now_day+'000000'
        tempflag2=now_day+'235959'
        flag1=int(tempflag1)
        flag2=int(tempflag2)
        data=db.session.query(Instruction.buy_sell_flag, Instruction.stock_id, Instruction.target_price, Instruction.total_amount, Instruction.target_number, Instruction.actual_number, Instruction.instruction_state, Instruction.time, Stock.stock_name).join(Stock).filter(Instruction.stock_id==Stock.stock_id and Instruction.fund_account_number==fund_acc_num and Instruction.time>flag1 and Instruction.time<flag2).all()
        res = []
        content = {}
        for i in data:
            content = {"flag": i[0], "id": i[1], "tprice": i[2], "amount": i[3], "tnum": i[4], "anum": i[5], "state": i[6], "time": i[7], "name": i[8]}
            res.append(content)
        print(res)
        return res
    
    @staticmethod
    def do_do_withdraw(fund_acc_num, keys):
        thiskeys=str(keys).split(",")
        n=len(thiskeys)
        for i in range(n):
            mykey=int(thiskeys[i])
            print(mykey)
            thisone=Instruction.query.filter(Instruction.time==mykey and Instruction.fund_account_number==fund_acc_num).one()
            if(thisone.instruction_state=='N' or thisone.instruction_state=='P'):
                if(thisone.buy_sell_flag=='B'):
                    money=thisone.target_price*thisone.target_number-thisone.total_amount
                    print(money)
                    moneyone=FundAccount.query.filter(FundAccount.fund_account_number==fund_acc_num).one()
                    print(moneyone.frozen)
                    moneyone.frozen -= money
                    print(moneyone.frozen)
                    thisone.instruction_state='E'
                    db.session.commit()
                    return 0
                else:
                    stocknum=thisone.target_number-thisone.actual_number
                    stockid=thisone.stock_id
                    ser_num=db.session.query(FundAccount.securities_account_number).filter(FundAccount.fund_account_number==fund_acc_num).one()
                    stockone=OwnStock.query.filter(OwnStock.stock_id==stockid and OwnStock.securities_account_number==ser_num).one()
                    print(stocknum)
                    print(stockone.frozen)
                    stockone.frozen -=stocknum
                    print(stockone.frozen)
                    thisone.instruction_state='E'
                    db.session.commit()
                    return 0
                    
            elif(thisone.instruction_state=='E'):
                return 1
            else:
                return 2        
                