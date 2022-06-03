from dao.con_auc_dao import ConAucDao
import datetime

class ConAuc:
    #指令预处理
    @staticmethod
    def continue_instruction_pretreatment(ins_id):
        # 检测股票状态
        ins = ConAucDao.getins(ins_id)  # 获取指令信息
        s = ConAucDao.getstock(ins)  # 获取股票信息
        if s.stock_status == 'F':  # 股票状态为'F'则返回
            ConAucDao.setexp(ins)  # 股票异常，设置为过期指令   ！！！！
            # return -1                      #股票状态异常，无法交易

        # 判断涨跌幅
        k = ConAucDao.getyesterdayk(s.stock_id)  # 获取昨日K值表
        if ins.target_price > (k.end_price) * (1 + s.rise_threshold) or ins.target_price < (k.end_price) * (
                1 - s.fall_threshold):
            ConAucDao.setexp(ins.instruction_id)  # 指令设置为过期
            # return -1                                 #指令出价超过涨跌幅，无法交易
    
    #连续竞价
    @staticmethod
    def continue_auction(inst_id):
        buy = ConAucDao.getbuyinstr(inst_id)
        sell = ConAucDao.getsellinstr(inst_id)
        if buy.target_price < sell.target_price:
            return -1    ##无法交易标志
        else:
            transaction_price = 0.5 * (buy.target_price + sell.target_price)
            buyrest = buy.target_number - buy.actual_number
            sellrest = sell.target_number - sell.actual_number
            transaction_number = min(buyrest, sellrest)
            con_res = [buy.instruction_id, sell.instruction_id, transaction_price, transaction_number]
            return con_res

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
    def createtransres(con_res):
        b_id = con_res[0]
        s_id = con_res[1]
        t_price = con_res[2]
        t_number = con_res[3]
        stock_id = ConAucDao.gettransstock(b_id)
        b_s_flag1 = ConAucDao.gettransflag(b_id)
        b_s_flag2 = ConAucDao.gettransflag(s_id)
        a_number1 = ConAucDao.gettransaccount(b_id)
        a_number2 = ConAucDao.gettransaccount(s_id)
        t_amount = t_price * t_number
        t_date = ConAucDao.getnowdata()
        t_time = ConAucDao.getnowtime()
        i_id1 = ConAucDao.gettransinstr(b_id)
        i_id2 = ConAucDao.gettransinstr(s_id)
        t1_id = ConAucDao.updatetransinfo(stock_id, b_s_flag1, a_number1, t_price,
                        t_amount, t_number, t_date, t_time, i_id1)
        t2_id = ConAucDao.updatetransinfo(stock_id, b_s_flag2, a_number2, t_price,
                        t_amount, t_number, t_date, t_time, i_id2)
        t_id = [t1_id, t2_id]
        return t_id
    
    #更新数据
    @staticmethod
    def update(t_id):
        # update stock price
        t_price = ConAucDao.gettransprice(t_id)
        s_id = ConAucDao.getstockid(t_id)
        ConAucDao.updatestockprice(s_id, t_price)

        # update K table
        date = ConAucDao.getstockid(t_id)
        k_info = ConAucDao.getkinfo(s_id, date)
        h_pri = k_info.highest_price
        l_pri = k_info.lowest_price
        k_id = k_info.k_id

        if (h_pri == None):
            ConAucDao.updatestartprice(k_id, t_price)

        ConAucDao.updateendprice(k_id, t_price)

        if (t_price > h_pri or h_pri == None):
            ConAucDao.updatehighestprice(k_id, t_price)

        if (t_price < l_pri or l_pri == None):
            ConAucDao.updatelowestprice(k_id, t_price)

        # update instruction
        i_id = ConAucDao.getinstid(t_id)
        t_number = ConAucDao.getinstnumber(t_id)
        t_amount = ConAucDao.getinstamount(t_id)
        ConAucDao.updateinstinfo(i_id, t_number, t_amount)

        i_info = ConAucDao.getinstinfo(i_id)
        t_num = i_info.target_number
        a_num = i_info.actual_number

        if (t_num == a_num):
            flag = 'T'
        else:
            flag = 'P'

        ConAucDao.updateinsttype(i_id, flag)