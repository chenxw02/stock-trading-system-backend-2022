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
        ConAuc.update(t_id[0])
        ConAuc.update(t_id[1])
        tran_list0 = (t_id[0])[:3] + (t_id[0])[4:6]
        tran_list1 = (t_id[1])[:3] + (t_id[1])[4:6]
        TradeService.update(tran_list0)
        TradeService.update(tran_list1)
        return t_id
