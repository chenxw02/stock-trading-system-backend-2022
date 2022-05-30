from model.center_trade import K
from model.center_trade import Stock
from model.center_trade import Transaction
from sqlalchemy import and_
import time

class AggInsPreDao:

    #处理过期指令
    @staticmethod
    def dealexpins():
        localtime = time.asctime(time.localtime(time.time()))
        localtime = time.strftime("%Y%m%d", time.localtime())
        tmp_time = int(localtime)
        tmp_time = tmp_time*1000000
        exp_ins = Instruction.query.filter(Instruction.time < tmp_time).all()
        exp_ins.instruction_state = "E"  # 设置指令为过期状态
        db.session.commit()

    #获取昨日K值表
    @staticmethod
    def getyesterdayk(stock_id):
        localtime = time.asctime(time.localtime(time.time()))
        localtime = time.strftime("%Y%m%d", time.localtime())
        inttime = int(localtime)
        tmpk = K.query.filter(_and(K.stock_id == i.stock_id, K.date < inttime))
        tmpk = tmpk.query.order_by(desc("date")).first()
        return tmpk

    #建立K值表
    @staticmethod
    def createktable(self):
        localtime = time.asctime(time.localtime(time.time()))
        localtime = time.strftime("%Y%m%d", time.localtime())
        inttime = int(localtime)
        sto = Stock.query.all()
        for i in sto:
            tmpkid = localtime+i.stock_id
            tmpk = K.query.filter(K.stock_id == i.stock_id)
            tmpk = tmpk.query.order_by(desc("date")).first()
            k = K()
            k.k_id = tmpkid
            k.stock_id = i.stock_id
            k.start_price = tmpk.start_price
            k.end_price = tmp.k.end_price
            k.trade_number = 0
            k.trade_amount = 0
            k.date = inttime
            session.add(k)
            session.commit()

    #获取股票信息
    @staticmethod
    def getstock(ins):
        s = Stock.query.filter(Stock.stock_id == ins.stock_id)
        return s

    #获取指令
    @staticmethod
    def getins(ins_id):
        ins = Instruction.query.filter(Instruction.instruction.id == ins_id)
        return

    #获取今日指令
    @staticmethod
    def gettodayins():
        localtime = time.asctime(time.localtime(time.time()))
        localtime = time.strftime("%Y%m%d", time.localtime())
        inttime = int(localtime)
        inttime = inttime*1000000
        ins = Instruction.query.filter(Instruction.time > inttime)
        return ins