from exts import db
from model.agg_auc import Instruction
from sqlalchemy import and_


class AggAucDao:
    @staticmethod
    def getbuyinstr(stock_id):
        buy = Instruction.query.filter(and_(Instruction.buy_sell_flag == 'B', Instruction.instruction_state == 'N',
                                            Instruction.stock_id == stock_id)).order_by('-target_price')
        return buy

    @staticmethod
    def getsellinstr(stock_id):
        sell = Instruction.query.filter(and_(Instruction.buy_sell_flag == 'S', Instruction.instruction_state == 'N',
                                             Instruction.stock_id == stock_id)).order_by('-target_price')
        sell.reserve()  # 卖价从低到高排序
        return sell

    @staticmethod
    def getstockid():
        record = Instruction.query.filter(and_(Instruction.instruction_state == 'N')).all()
        s_id = []
        for r in record:
            if r.stock_id not in s_id:
                s_id.append(r.stock_id)
        return s_id
