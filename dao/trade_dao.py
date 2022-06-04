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
    def check_transaction(sID, tType, price, amount, uID):
        price = float(price)
        amount = int(amount)

        data = db.session.query(Stock.stock_id).filter(Stock.stock_id == sID).all()
        if len(data) == 0:  # if stockID does not exist
            return 1
        data = db.session.query(Stock.stock_id).filter(and_(Stock.stock_id == sID, Stock.stock_status != 'F')).all()
        if len(data) == 0:  # if stockID exists but the stock cannot be traded
            return 2

        kvals = db.session.query(K.k_id, K.stock_id, K.end_price, K.date).filter(K.stock_id == sID).all()
        kvals.sort(key=lambda a: a[3], reverse=True)  # find last days ending price
        type = db.session.query(Stock.stock_type).filter(Stock.stock_id == sID).all()[0][0]  # find stock type

        # calculate the minimum price according to the stock type
        if (type == 'S'):
            min_price = kvals[0][2] + (kvals[0][2] * 0.05)
        else:
            min_price = kvals[0][2] + (kvals[0][2] * 0.1)

        if price < min_price and tType == 'buy':  # if the buying price is too low
            return 3

        if tType == 'buy':
            funds = db.session.query(FundAccount.balance, FundAccount.frozen, FundAccount.taken) \
                .filter(FundAccount.fund_account_number == uID).first()

            available = funds[0] - funds[1] - funds[2]
            total_price = price * amount
            if available < total_price:  # if the user does not have enough funds for the transaction
                return 4
        else:
            stock_own = db.session.query(OwnStock.own_number, OwnStock.frozen) \
                .filter(and_(OwnStock.stock_id == sID, OwnStock.securities_account_number == uID)).all()[0]

            stock_own_count = stock_own[0] - stock_own[1]

            if stock_own_count < amount:  # if the user does not have enough stock for the transaction
                return 5

        return 0  # else all is well

    @staticmethod
    def create_instruction(sID, tType, price, amount, uID):
        price = float(price)
        amount = int(amount)

        if tType == 'buy':
            tType = 'B'
        else:
            tType = 'S'

        new_tID = int(db.session.query(func.max(Instruction.instruction_id)).first()[0]) + 1
        print(new_tID)
        time = int(datetime.datetime.now().strftime('%d'))
        if new_tID is None:
            new_tID = 1
        newInstruction = Instruction()
        newInstruction.instruction_id = new_tID
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
    def freeze_assets(sID, tType, price, amount, uID):
        price = float(price)
        amount = int(amount)
        if tType == 'buy':
            totalPrice = price * amount
            funds = FundAccount.query.filter(FundAccount.fund_account_number == uID).first()
            funds.frozen += totalPrice
            db.session.commit()
        else:
            stock_own = OwnStock.query.filter(
                and_(OwnStock.stock_id == sID, OwnStock.securities_account_number == uID)).first()
            stock_own.frozen += amount

    @staticmethod
    def get_fund_info(fund_acc_num):
        data = db.session.query(FundAccount.balance, FundAccount.frozen, FundAccount.taken).filter(
            FundAccount.fund_account_number == fund_acc_num).all()
        # 获取当日日期
        now_date = int(datetime.datetime.now().strftime('%Y%m%d'))
        data2 = db.session.query(func.sum(Transaction.transaction_amount)).filter(
            and_(Transaction.transaction_date == now_date, Transaction.fund_account_number == fund_acc_num,
                 Transaction.buy_sell_flag == 'S')).all()
        if data2[0][0] is None:
            data2 = 0
        else:
            data2 = data2[0][0]
        res = {"fund_account_number": fund_acc_num, "balance": data[0][0], "frozen": data[0][1], "taken": data[0][2],
               "sellamount": data2}
        return res

    @staticmethod
    def get_own_stock_info(fund_acc_num):
        # 查询证券账户号码
        data = db.session.query(FundAccount.securities_account_number).filter(
            FundAccount.fund_account_number == fund_acc_num).all()
        acc = data[0][0]
        data2 = db.session.query(OwnStock.own_number, OwnStock.frozen, OwnStock.own_amount, Stock.stock_name,
                                 Stock.stock_id, Stock.price).join(OwnStock,
                                                                   OwnStock.stock_id == Stock.stock_id).filter(
            OwnStock.securities_account_number == acc).order_by(Stock.stock_name).all()
        res = []
        content = {}
        # 生成需要返回的结果
        for i in data2:
            content = {"own_number": i[0], "frozen": i[1], "own_amount": i[2], "stock_name": i[3], "stock_id": i[4],
                       "price": i[5]}
            res.append(content)
        return res

    @staticmethod
    def update(sid, fund_acc_num, buy_sell_flag, amount, num):
        # 查询证券账户号码
        sec = db.session.query(FundAccount.securities_account_number).filter(
            FundAccount.fund_account_number == fund_acc_num).all()[0][0]

        fund_acc = FundAccount.query.filter(FundAccount.fund_account_number == fund_acc_num).first()
        own_stock = OwnStock.query.filter(
            and_(OwnStock.securities_account_number == sec, OwnStock.stock_id == sid)).first()

        if buy_sell_flag == 'S':  # 卖
            fund_acc.taken -= amount
            fund_acc.frozen -= amount

            own_stock.own_number -= num
            own_stock.frozen -= num
            own_stock.own_amount -= amount
            if own_stock.own_number == 0:  # 股票已全部卖出
                db.session.delete(own_stock)
        else:  # 买
            fund_acc.taken += amount
            fund_acc.frozen -= amount

            if own_stock is None:  # own_stock里没有该股票的记录
                data = OwnStock(stock_id=sid, securities_account_number=sec, own_number=num, frozen=0,
                                own_amount=amount)
                db.session.add(data)
            else:
                own_stock.own_number += num
                own_stock.own_amount += amount
        db.session.commit()