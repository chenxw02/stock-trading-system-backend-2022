from exts import db
from model.agg_auc import Instruction
from model.agg_auc import K
from model.agg_auc import Stock
from model.agg_auc import Transaction
from sqlalchemy import and_


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

