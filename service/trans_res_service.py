import datetime
from dao.trans_res_dao import TransResDao
from model.trans_res import Instruction


class TransResService:
    # 获取日期时间
    @staticmethod
    def getnowdata():
        now = datetime.datetime.now()
        s = now.strftime('%Y%m%d')
        data = int(s, 10)
        return data

    @staticmethod
    def getnowtime():
        now = datetime.datetime.now()
        s = now.strftime('%H%M%S')
        time = int(s, 10)
        return time

    # 生成交易结果
    @staticmethod
    def createtransres(b_id, s_id, t_price, t_number):
        stock_id = gettransstock(b_id)
        b_s_flag1 = gettransflag(b_id)
        b_s_flag2 = gettransflag(s_id)
        a_number1 = gettransaccount(b_id)
        a_number2 = gettransaccount(s_id)
        t_amount = t_price*t_number
        t_date = getnowdata()
        t_time = getnowtime()
        i_id1 = gettransinstr(b_id)
        i_id2 = gettransinstr(s_id)
        updatetransinfo(stock_id, b_s_flag1, a_number1, t_price,
                        t_amount, t_number, t_date, t_time, i_id1)
        updatetransinfo(stock_id, b_s_flag2, a_number2, t_price,
                        t_amount, t_number, t_date, t_time, i_id2)
        return
