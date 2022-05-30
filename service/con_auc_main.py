from dao.con_auc_dao import ConAucDao
import datetime
from service.con_auc_service import ConAuc


class ConAucService:

    @staticmethod
    def con_auc(inst_id):
        # 预处理
        #
        #

        # 连续竞价
        con_res = ConAuc.continue_auction(inst_id)
        if con_res == -1:  ##没有任何成交
            return -1

        # 声称结果
        t_id = ConAuc.createtransres(con_res)

        # 更新数据
        ConAuc.update(t_id)
        ConAuc.update(t_id)

        return t_id
