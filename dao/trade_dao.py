from exts import db
from model.account_admin import FundAccount
from model.account_admin import OwnStock
from model.center_trade import Stock
from model.center_trade import Transaction
from sqlalchemy import and_
from sqlalchemy import func
import datetime

# 将一个表的所有简单操作集中成一个dao数据库类
class TradeDao:
    @staticmethod
    def get_fund_info(fund_acc_num):
        data = db.session.query(FundAccount.balance, FundAccount.frozen, FundAccount.taken).filter(FundAccount.fund_account_number == fund_acc_num).all()
        now_date = int(datetime.datetime.now().strftime('%Y%m%d'))
        data2 = db.session.query(func.sum(Transaction.transaction_amount)).filter(and_(Transaction.transaction_date == now_date, Transaction.fund_account_id == fund_acc_num, Transaction.buy_sell_flag == 'S')).all()
        res = {"balance": data[0][0], "frozen": data[0][1], "taken": data[0][2], "sellamount": data2[0][0]}
        return res

    @staticmethod
    def get_own_stock_info(fund_acc_num):
        data = db.session.query(FundAccount.securities_account_number).filter(FundAccount.fund_account_number == fund_acc_num).all()
        acc = data[0][0]
        data2 = db.session.query(OwnStock.own_number, OwnStock.frozen, OwnStock.own_amount, Stock.stock_name, Stock.stock_id, Stock.price).join(OwnStock, OwnStock.stock_id == Stock.stock_id).filter(OwnStock.securities_account_number == acc).order_by(Stock.stock_name).all()
        res = []
        content = {}
        for i in data2:
            content = {"own_number": i[0], "frozen": i[1], "own_amount": i[2], "stock_name": i[3], "stock_id": i[4], "price": i[5]}
            res.append(content)
        return res

    @staticmethod
    def update_fund_acc(trans_id):
        data = db.session.query(Transaction.fund_account_number, Transaction.transaction_amount).filter(Transaction.transaction_id == trans_id).all()
        fund_acc_num = data[0][0]
        trans_amt = data[0][1]
        ret = db.session.query.filter(FundAccount.fund_account_number == fund_acc_num).update({FundAccount.taken: FundAccount.taken-trans_amt, FundAccount.frozen: FundAccount.frozen-trans_amt})
        db.session.commit()
    
    @staticmethod
    def update_own_stock(trans_id):
        data = db.session.query(Transaction.fund_account_number, Transaction.stock_id, Transaction.transaction_number, Transaction.transaction_amount).filter(Transaction.transaction_id == trans_id).all()
        fund_acc_num, sid, num, amt = data[0][0], data[0][1], data[0][2], data[0][3]
        sec_acc_num = db.session.query(FundAccount.securities_account_number).filter(FundAccount.fund_account_number == fund_acc_num).all()[0][0]
        ret = db.session.query.filter(and_(OwnStock.securities_account_number == sec_acc_num, OwnStock.stock_id == sid)).update({OwnStock.own_number: OwnStock.own_number-num, OwnStock.frozen: OwnStock.own_number-num, OwnStock.own_amount: OwnStock.own_amount-amt})
        db.session.commit()