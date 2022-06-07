from flask import jsonify
from exts import db
from model.center_trade import Stock
from model.center_trade import K
from model.center_trade import Transaction
from sqlalchemy import or_
from sqlalchemy import and_
import datetime

class ReleaseSearchDao:
    @staticmethod
    def get1(name):
        ret1 = {}
        #ret = Stock.query.filter(or_(Stock.stock_id==name, Stock.stock_name==name)).all()
        ret1 = db.session.query(Stock.stock_id, Stock.stock_name, Stock.price).filter(or_(Stock.stock_id==name, Stock.stock_name.like("%{}%".format(name)))).all()
        payload = []
        content = {}
        print (ret1)
        for i in ret1:
            #content = {'stock_id': i[0], 'stock_name': i[1]}
            #now_date = int(datetime.datetime.now().strftime('%Y%m%d'))
            #print(now_date)
            ret2 = {}
            ret3 = {}
            ret2 = db.session.query(K.start_price, K.end_price, K.highest_price, K.lowest_price).filter(K.stock_id==i[0]).order_by(K.date.desc()).all()
            #ret3 = db.session.query(Transaction.buy_sell_flag, Transaction.transaction_price, Transaction.transaction_amount, Transaction.transaction_number, Transaction.transaction_date, Transaction.transaction_time).filter(Transaction.stock_id==i[0]).order_by(Transaction.transaction_date.desc()).all()
            ret3 = db.session.query(Transaction.buy_sell_flag, Transaction.transaction_price, Transaction.transaction_amount, Transaction.transaction_number, Transaction.transaction_date, Transaction.transaction_time).filter(and_(Transaction.stock_id==i[0], Transaction.buy_sell_flag=='B')).order_by(Transaction.transaction_date.desc(), Transaction.transaction_time.desc()).all()
            #print(ret2)
            #print(ret3)
            for j in ret2:
                count = 0
                for k in ret3:
                    count = count + 1
                    if (count > 5):
                        break
                    content = {'stock_id': i[0], 'stock_name': i[1], 'start_price': j[0], 'end_price': i[2], 'highest_price': j[2], 'lowest_price': j[3], 'buy_sell_flag': k[0], 'transaction_price': k[1], 'transaction_amount': k[2], 'transaction_number': k[3], 'transaction_date': k[4], 'transaction_time': k[5]}
                    if (len(content)==0):
                        continue
                    payload.append(content)
                    content = {}
                if (len(ret3) == 0):
                    content = {'stock_id': i[0], 'stock_name': i[1], 'start_price': j[0], 'end_price': i[2], 'highest_price': j[2], 'lowest_price': j[3], 'buy_sell_flag': '', 'transaction_price': '', 'transaction_amount': '', 'transaction_number': '', 'transaction_date': '', 'transaction_time': ''}
                    if (len(content)==0):
                        continue
                    payload.append(content)
                    content = {}
                break
            if (len(ret2) == 0):
                content = {'stock_id': i[0], 'stock_name': i[1], 'start_price': '', 'end_price': i[2], 'highest_price': '', 'lowest_price': '', 'buy_sell_flag': '', 'transaction_price': '', 'transaction_amount': '', 'transaction_number': '', 'transaction_date': '', 'transaction_time': ''}
                if (len(content)==0):
                    continue
                payload.append(content)
                content = {}

        print (payload)
        return payload
    
    @staticmethod
    def get2(name):
        ret = {}
        ret = db.session.query(K.start_price, K.end_price, K.highest_price, K.lowest_price, K.date).filter(K.stock_id==name).order_by(K.date.desc()).all()
        payload = []
        content = {}
        for i in ret:
            content = {'date': i[4], 'start_price': i[0], 'end_price': i[1], 'highest_price': i[2], 'lowest_price': i[3]}
            payload.append(content)
            content = {}
        print (payload)
        return payload