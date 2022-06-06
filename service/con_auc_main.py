from dao.con_auc_dao import ConAucDao
import datetime
from service.con_auc_service import ConAuc
from service.trade_service import TradeService

class ConAucService:

    @staticmethod
    def con_auc(inst_id):
        # print(inst_id)
        # 预处理
        ConAuc.continue_instruction_pretreatment(inst_id)
        # 连续竞价
        con_res = ConAuc.continue_auction(inst_id)
        # print(con_res)
        if con_res == -1:  ##没有任何成交
            return -1
        # 生成结果
        t_id = ConAuc.createtransres(con_res)
        # 更新数据
        ConAuc.update(t_id[0].transaction_id)
        ConAuc.update(t_id[1].transaction_id)
        tran_list0 = [t_id[0].stock_id, t_id[0].fund_account_number, t_id[0].buy_sell_flag, t_id[0].transaction_amount, t_id[0].transaction_number, t_id[0].instruction_id]
        tran_list1 = [t_id[1].stock_id, t_id[1].fund_account_number, t_id[1].buy_sell_flag, t_id[1].transaction_amount, t_id[1].transaction_number, t_id[1].instruction_id]
        print(tran_list0)
        TradeService.update(tran_list0[0], tran_list0[1], tran_list0[2], tran_list0[3], tran_list0[4], tran_list0[5])
        TradeService.update(tran_list1[0], tran_list1[1], tran_list1[2], tran_list1[3], tran_list1[4], tran_list0[5])
        return t_id
