from exts import db
from model.center_trade import Instruction
from model.center_trade import K
from model.center_trade import Stock
from model.center_trade import Transaction
from sqlalchemy import and_
import time


class AggAucDao:
    @staticmethod
    def getbuyinstr(stock_id):
        buy = Instruction.query.filter(and_(Instruction.buy_sell_flag == 'B', Instruction.instruction_state == 'N',
                                            Instruction.stock_id == stock_id)).order_by('-target_price')
        return buy

    @staticmethod
    def getsellinstr(stock_id):
        sell = Instruction.query.filter(and_(Instruction.buy_sell_flag == 'S', Instruction.instruction_state == 'N',
                                             Instruction.stock_id == stock_id)).order_by('-target_price')
        sell.reserve()  # 卖价从低到高排序
        return sell

    @staticmethod
    def getstockid():
        record = Instruction.query.filter(and_(Instruction.instruction_state == 'N')).all()
        s_id = []
        for r in record:
            if r.stock_id not in s_id:
                s_id.append(r.stock_id)
        return s_id

    # update data
    @staticmethod
    def gettransprice(trans_id):
        trans = Transaction.query.filter(Transaction.transaction_id == trans_id)
        for i in trans:
            price = i.transaction_price
        return price

    @staticmethod
    def gettransdate(trans_id):
        trans = Transaction.query.filter(Transaction.transaction_id == trans_id)
        for i in trans:
            date = i.transaction_date
        return date

    @staticmethod
    def getstockid(trans_id):
        trans = Transaction.query.filter(Transaction.transaction_id == trans_id)
        for i in trans:
            s_id = i.stock_id
        return s_id


    @staticmethod
    def updatestockprice(s_id, price):
        s_info = Stock.query.filter(Stock.stock_id == s_id)
        for i in s_info:
            i.price = price
            db.session.commit()

    @staticmethod
    def getkinfo(stock_id, date):
        k_info = K.query.filter(and_(K.date == date, K.stock_id == stock_id))
        return k_info

    @staticmethod
    def updatestartprice(k_id, price):
        k_info = K.query.filter(K.stock_id == k_id)
        for i in k_info:
            i.start_price = price
            db.session.commit()

    @staticmethod
    def updateendprice(k_id, price):
        k_info = K.query.filter(K.stock_id == k_id)
        for i in k_info:
            i.end_price = price
            db.session.commit()

    @staticmethod
    def updatehighestprice(k_id, price):
        k_info = K.query.filter(K.stock_id == k_id)
        for i in k_info:
            i.highest_price = price
            db.session.commit()

    @staticmethod
    def updatelowestprice(k_id, price):
        k_info = K.query.filter(K.stock_id == k_id)
        for i in k_info:
            i.lowest_price = price
            db.session.commit()

    @staticmethod
    def getinstid(trans_id):
        trans = Transaction.query.filter(Transaction.transaction_id == trans_id)
        for i in trans:
            i_id = i.instruction_id
        return i_id

    @staticmethod
    def getinstamount(trans_id):
        trans = Transaction.query.filter(Transaction.transaction_id == trans_id)
        for i in trans:
            amount = i.transaction_amount
        return amount

    @staticmethod
    def getinstnumber(trans_id):
        trans = Transaction.query.filter(Transaction.transaction_id == trans_id)
        for i in trans:
            number = i.transaction_number
        return number

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
        return i_info

    @staticmethod
    def updateinsttype(i_id, state):
        i_info = Stock.query.filter(Instruction.instruction_id == i_id)
        for i in i_info:
            i.instruction_state = state
            db.session.commit()

   # 获取股票编号
    @staticmethod
    def gettransstock(instr_id):
        instr = Instruction.query.filter(Instruction.stock_id == instr_id)
        return instr.stock_id

    # 获取买卖标志
    @staticmethod
    def gettransflag(instr_id):
        instr = Instruction.query.filter(Instruction.stock_id == instr_id)
        return instr.buy_sell_flag

    # 获取账户编号
    @staticmethod
    def gettransaccount(instr_id):
        instr = Instruction.query.filter(Instruction.stock_id == instr_id)
        return instr.fund_account_number

    # 获取指令编号
    @staticmethod
    def gettransinstr(instr_id):
        instr = Instruction.query.filter(Instruction.stock_id == instr_id)
        return instr.instruction_id

    # 生成交易结果
    @staticmethod
    def updatetransinfo(s_id, b_s_flag, a_number, t_price, t_amount, t_number, t_date, t_time, i_id):
        trans = Transaction()
        trans.stock_id = s_id
        trans.buy_sell_flag = b_s_flag
        trans.fund_account_number = a_number
        trans.transaction_price = t_price
        trans.transaction_amount = t_amount
        trans.transaction_number = t_number
        trans.transaction_date = t_date
        trans.transaction_time = t_time
        trans.instruction_id = i_id
        db.session.add(trans)
        db.session.commit()
        return trans.transaction_id

    #处理过期指令
    @staticmethod
    def dealexpins():
        localtime = time.strftime("%Y%m%d", time.localtime())
        tmp_time = int(localtime)
        tmp_time = tmp_time*1000000
        exp_ins = Instruction.query.filter(Instruction.time < tmp_time).all()
        for i in exp_ins:
            i.instruction_state = "E"  # 设置指令为过期状态
            db.session.commit()

    #获取昨日K值表
    @staticmethod
    def getyesterdayk(stock_id):
        localtime = time.strftime("%Y%m%d", time.localtime())
        inttime = int(localtime)
        tmp_k = K.query.filter(K.stock_id == stock_id, K.date < inttime)
        k = tmp_k.query.order_by(db.desc(tmp_k.date)).first()
        return k

    #建立K值表
    @staticmethod
    def createktable():
        localtime = time.strftime("%Y%m%d", time.localtime())
        inttime = int(localtime)
        sto = Stock.query.all()
        for i in sto:
            tmpkid = localtime+i.stock_id
            tmpk = K.query.filter(K.stock_id == i.stock_id)
            tmpk = tmpk.query.order_by(db.desc(tmpk.date)).first()
            k = K()
            k.k_id = tmpkid
            k.stock_id = i.stock_id
            k.start_price = tmpk.start_price
            k.end_price = tmpk.end_price
            k.trade_number = 0
            k.trade_amount = 0
            k.date = inttime
            db.session.add(k)
            db.session.commit()

    #获取股票信息
    @staticmethod
    def getstock(ins):
        s = Stock.query.filter(Stock.stock_id == ins.stock_id)
        return s

    #获取指令
    @staticmethod
    def getins(ins_id):
        ins = Instruction.query.filter(Instruction.instruction.id == ins_id)
        return ins

    #获取今日指令
    @staticmethod
    def gettodayins():
        localtime = time.strftime("%Y%m%d", time.localtime())
        inttime = int(localtime)
        inttime = inttime*1000000
        ins = Instruction.query.filter(Instruction.time > inttime)
        return ins

    #设置指令过期
    @staticmethod
    def setexp(ins_id):
        ins = Instruction.query.filter(Instruction.instruction_id == ins_id)
        ins.instruction_state = "E"
        db.session.commit()