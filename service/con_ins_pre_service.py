from dao.con_ins_pre_dao import ConInsPreDao
from model.center_trade import Instruction
from model.center_trade import K
from model.center_trade import Stock
import time

class ConInsPreService:

    @staticmethod
    def continue_instruction_pretreatment(ins_id):
        #检测股票状态
        ins = ConInsPreDao.getins(ins_id)  #获取指令信息
        s = ConInsPreDao.getstock(ins)     #获取股票信息
        if s.stock_status == 'F':          #股票状态为'F'则返回
            ConInsPreDao.setexp(ins)       #股票异常，设置为过期指令   ！！！！
            #return -1                      #股票状态异常，无法交易

        #判断涨跌幅
        k = ConInsPreDao.getyesterdayk(s.stock_id)     #获取昨日K值表
        if ins.target_price>(k.end_price)*(1+s.rise_threshold) or ins.target_price<(k.end_price)*(1-s.fall_threshold):
            ConInsPreDao.setexp(ins.instruction_id)    #指令设置为过期
            #return -1                                 #指令出价超过涨跌幅，无法交易