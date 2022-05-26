from dao.agg_auc_dao import AggAucDao
from model.agg_auc import Instruction


class AggAucService:
    @staticmethod
    def aggregate_auction():
        s_id = AggAucDao.getstockid()
        t_record = []  # 总的交易记录列表
        r_last_cnt = 0  # 记录表中之前的项数
        for sid in s_id:
            buy = AggAucDao.getbuyinstr(sid)     # 买指令价格从高到低排序
            sell = AggAucDao.getsellinstr(sid)   # 卖指令价格从低到高排序
            bf = 0  # 买指令index
            sf = 0  # 卖指令index
            # 买卖指令都存在时
            while bf < len(buy) and sf < len(sell):
                b = buy[bf]
                s = sell[sf]
                price = 0.0
                # 买价>=卖价，可以撮合
                if b.target_price >= s.target_price:
                    min_num = min(b.target_number, s.target_number)
                    price = 0.5 * (b.target_price + s.target_price)  # 中间价格计算
                    record = [b.instruction_id, s.instruction_id, min_num]  # 暂时先不插入最终成交价格
                    t_record.append(record)  # 将记录加入总表
                    b.target_number = b.target_number - min_num  # 更新股票数量
                    s.target_number = s.target_number - min_num
                    if b.target_number == 0:  # 指针后移
                        bf = bf + 1
                    if s.target_number == 0:
                        sf = sf + 1
                # 买价<卖价，撮合结束
                else:
                    break
            for i in range(r_last_cnt, len(t_record)):
                t_record[i].append(price)  # 插入最终的成交价
            r_last_cnt = len(t_record)
            # 更新数据表 待补充
        return t_record
