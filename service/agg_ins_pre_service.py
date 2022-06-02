from dao.agg_ins_pre_dao import AggInsPreDao
from model.center_trade import Instruction
from model.center_trade import K
from model.center_trade import Stock
import time

class InsPreDao:

    #处理过期指令
    @staticmethod
    def deal_expired_instruction():         #处理过期指令
        AggInsPreDao.dealexpins()

    #创建K值表
    @staticmethod
    def create_k_table():       #创建k值表
        AggInsPreDao.createktable()

    #判断股票状态
    @staticmethod
    def judge_stock_status():
        localtime = time.asctime(time.localtime(time.time()))
        localtime = time.strftime("%Y%m%d", time.localtime())
        inttime = int(localtime)
        instr = AggInsPreDao.gettodayins()
        for i in instr:
            s = AggInsPreDao.getstock(i)         #获取股票信息
            if s.stock_status=='F':              #股票状态为'F'则返回
                AggInsPreDao.setexp(i.instruction_id)            #设置指令为过期指令

    #判断涨跌幅
    @staticmethod
    def judge_rise_fall():
        instr = AggInsPreDao.gettodayins()
        for i in instr:
            s = AggInsPreDao.getstock(i.instruction_id)              #获取股票信息
            k = AggInsPreDao.getyesterdayk(s.stock_id)               #获取昨日K值表
            if i.target_price>(k.end_price)*(1+s.rise_threshold) or i.target_price<(k.end_price)*(1-s.fall_threshold):
                AggInsPreDao.setexp(i.instruction_id)                #出价不在涨跌幅范围内