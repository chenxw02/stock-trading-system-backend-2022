from dao.agg_auc_dao import AggAucDao
import datetime
from service.agg_auc_service import AggAuc


class AggAucService:

    @staticmethod
    def agg_auc(inst_id):
        # 预处理
        AggAuc.aggregate_instruction_pretreatment()
        # 连续竞价
        agg_res = AggAuc.aggregate_auction()
        # 生成结果
        for i in range(0, len(agg_res)):
            t_id = AggAuc.createtransres(agg_res[i])
        # 更新数据
            AggAuc.update(t_id[0])
            AggAuc.update(t_id[1])
            tran_list0 = (t_id[0])[:3] + (t_id[0])[4:6]
            tran_list1 = (t_id[1])[:3] + (t_id[1])[4:6]
            # update(tran_list0)
            # update(tran_list1)

        return
