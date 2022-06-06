import random

from exts import db
from model.center_trade import Transaction
from sqlalchemy import func
from model.center_trade import Instruction
from model.center_trade import K
from model.center_trade import Stock
from sqlalchemy import and_
from sqlalchemy import or_
import time

class ConAucDao:

    @staticmethod
    def updatekinfo(k_id, t_number, t_amount):
        k_info = K.query.filter(K.k_id == k_id)
        for i in k_info:
            i.trade_amount = i.trade_amount + t_amount
            i.trade_number = i.trade_number + t_number
            db.session.commit()

    # 获取昨日K值表
    @staticmethod
    def getyesterdayk(stock_id):
        localtime = time.asctime(time.localtime(time.time()))
        localtime = time.strftime("%Y%m%d", time.localtime())
        inttime = int(localtime)
        tmp_k = K.query.filter(and_(K.stock_id == stock_id, K.date < inttime)).order_by(db.desc(K.date)).first()
        return tmp_k

    # 获取股票信息
    @staticmethod
    def getstock(ins):
        s = Stock.query.filter(Stock.stock_id == ins.stock_id)
        return s[0]

    # 获取指令信息
    @staticmethod
    def getins(ins_id):
        ins = Instruction.query.filter(Instruction.instruction_id == ins_id)
        return ins[0]

    # 设置不在涨跌幅阈值内的指令为过期指令
    @staticmethod
    def setexp(ins_id):
        ins = Instruction.query.filter(Instruction.instruction_id == ins_id)
        ins[0].instruction_state = "E"
        db.session.commit()

    #获取买指令
    @staticmethod
    def getbuyinstr(inst_id):
        # print(inst_id)
        temp = Instruction.query.filter(Instruction.instruction_id == inst_id).all()
        # print(temp)
        # print(temp[0].instruction_id)
        sto_id = temp[0].stock_id
        buy = Instruction.query.filter(and_(Instruction.buy_sell_flag=='B',
                                            Instruction.stock_id==sto_id)).filter(or_(Instruction.instruction_state=='N', Instruction.instruction_state=='P')).order_by(db.desc(Instruction.target_price)).all()
        # print(buy[0].instruction_id)
        return buy
        # if len(buy) == 1:
        #     return buy
        # else:
        #     earlybuy = Instruction()
        #     earlybuy.time = 999999
        #     for x in buy:
        #         if x.time < earlybuy.time:
        #             earlybuy = x
        #     return earlybuy

    #获取卖指令
    @staticmethod
    def getsellinstr(inst_id):
        temp = Instruction.query.filter(Instruction.instruction_id == inst_id).all()
        sto_id = temp[0].stock_id
        sell = Instruction.query.filter(and_(Instruction.buy_sell_flag=='S',
                                             Instruction.stock_id==sto_id)).filter(or_(Instruction.instruction_state=='N', Instruction.instruction_state=='P')).order_by(
            Instruction.target_price).all()
        return sell
        # if len(sell) == 1:
        #     return sell
        # else:
        #     earlysell = Instruction()
        #     earlysell.time = 999999
        #     for x in sell:
        #         if x.time < earlysell.time:
        #             earlysell = x
        #     return earlysell

    # 获取股票编号
    @staticmethod
    def gettransstock(instr_id):
        instr = Instruction.query.filter(Instruction.instruction_id == instr_id).all()
        return instr[0].stock_id

    # 获取买卖标志
    @staticmethod
    def gettransflag(instr_id):
        instr = Instruction.query.filter(Instruction.instruction_id == instr_id).all()
        return instr[0].buy_sell_flag

    # 获取账户编号
    @staticmethod
    def gettransaccount(instr_id):
        instr = Instruction.query.filter(Instruction.instruction_id == instr_id).all()
        return instr[0].fund_account_number

    # 获取指令编号
    @staticmethod
    def gettransinstr(instr_id):
        instr = Instruction.query.filter(Instruction.instruction_id == instr_id).all()
        return instr[0].instruction_id

    # 生成交易结果
    @staticmethod
    def updatetransinfo(s_id, b_s_flag, a_number, t_price, t_amount, t_number, t_date, t_time, i_id):
        trans = Transaction()
        trans.stock_id = s_id
        # print(trans.stock_id)
        trans.buy_sell_flag = b_s_flag
        trans.fund_account_number = a_number
        trans.transaction_price = t_price
        trans.transaction_amount = t_amount
        trans.transaction_number = t_number
        trans.transaction_date = t_date
        trans.transaction_time = t_time
        trans.instruction_id = i_id
        # trans.transaction_timestamp = "2022-06-05 16:24:34"
        # print(trans.transaction_id)
        trans.transaction_id = random.random()
        db.session.add(trans)
        db.session.commit()
        return trans.transaction_id

    # update data
    @staticmethod
    def gettransprice(trans_id):
        trans = Transaction.query.filter(Transaction.transaction_id == trans_id).all()
        return trans[0].transaction_price

    @staticmethod
    def getstockid(trans_id):
        trans = Transaction.query.filter(Transaction.transaction_id == trans_id).all()
        return trans[0].stock_id

    @staticmethod
    def gettrandate(trans_id):
        trans = Transaction.query.filter(Transaction.transaction_id == trans_id).all()
        return trans[0].transaction_date

    @staticmethod
    def updatestockprice(s_id, price):
        s_info = Stock.query.filter(Stock.stock_id == s_id)
        for i in s_info:
            i.price = price
            db.session.commit()

    @staticmethod
    def gettransdate(trans_id):
        trans = Transaction.query.filter(Transaction.transaction_id == trans_id)
        return trans[0].transaction_date

    @staticmethod
    def getkinfo(stock_id, date):
        # print(date)
        # print(stock_id)
        k_info = K.query.filter(and_(K.date == date, K.stock_id == stock_id)).all()
        return k_info[0]

    @staticmethod
    def updatestartprice(k_id, price):
        k_info = K.query.filter(K.k_id == k_id)
        for i in k_info:
            i.start_price = price
            db.session.commit()

    @staticmethod
    def updateendprice(k_id, price):
        k_info = K.query.filter(K.k_id == k_id)
        for i in k_info:
            i.end_price = price
            db.session.commit()

    @staticmethod
    def updatehighestprice(k_id, price):
        k_info = K.query.filter(K.k_id == k_id)
        for i in k_info:
            i.highest_price = price
            db.session.commit()

    @staticmethod
    def updatelowestprice(k_id, price):
        k_info = K.query.filter(K.k_id == k_id)
        for i in k_info:
            i.lowest_price = price
            db.session.commit()

    @staticmethod
    def getinstid(trans_id):
        trans = Transaction.query.filter(Transaction.transaction_id == trans_id)
        return trans[0].instruction_id

    @staticmethod
    def getinstamount(trans_id):
        trans = Transaction.query.filter(Transaction.transaction_id == trans_id)
        return trans[0].transaction_amount

    @staticmethod
    def getinstnumber(trans_id):
        trans = Transaction.query.filter(Transaction.transaction_id == trans_id)
        return trans[0].transaction_number

    @staticmethod
    def updateinstinfo(i_id, t_number, t_amount):
        i_info = Instruction.query.filter(Instruction.instruction_id == i_id)
        for i in i_info:
            i.total_amount = i.total_amount + t_amount
            i.actual_number = i.actual_number + t_number
            db.session.commit()

    @staticmethod
    def getinstinfo(i_id):
        i_info = Instruction.query.filter(Instruction.instruction_id == i_id)
        return i_info[0]

    @staticmethod
    def updateinsttype(i_id, state):
        # print(i_id)
        i_info = Instruction.query.filter(Instruction.instruction_id == i_id).all()
        # print(state)
        for i in i_info:
            i.instruction_state = state
            db.session.commit()