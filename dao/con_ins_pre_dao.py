from exts import db
from model.center_trade import Instruction
from model.center_trade import K
from model.center_trade import Stock
from sqlalchemy import and_
import time

class ConInsPreDao:

    #获取昨日K值表
    @staticmethod
    def getyesterdayk(stock_id):
        localtime = time.asctime(time.localtime(time.time()))
        localtime = time.strftime("%Y%m%d", time.localtime())
        inttime = int(localtime)
        tmp_k = K.query.filter(K.stock_id == stock_id, K.date < inttime)
        k = tmp_k.query.order_by(db.desc(tmp_k.date)).first()
        return k

    #获取股票信息
    @staticmethod
    def getstock(ins):
        s = Stock.query.filter(Stock.stock_id == ins.stock_id)
        return s

    #获取指令信息
    @staticmethod
    def getins(ins_id):
        ins = Instruction.query.filter(Instruction.instruction.id == ins_id)
        return ins

    #设置不在涨跌幅阈值内的指令为过期指令
    @staticmethod
    def setexp(ins_id):
        ins = Instruction.query.filter(Instruction.instruction_id == ins_id)
        ins.instruction_state = "E"
        db.session.commit()