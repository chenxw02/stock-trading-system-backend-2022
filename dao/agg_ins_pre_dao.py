from exts import db
from model.center_trade import K
from model.center_trade import Stock
from model.center_trade import Instruction
import time

class AggInsPreDao:

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