from exts import db
from model.con_auc import Instruction
from sqlalchemy import func
from sqlalchemy import and_


class ConAucDao:
    @staticmethod
    def getbuyinstr(inst_id):
        temp = Instruction.query.get(inst_id)
        sto_id = temp.stock_id
        buy = Instruction.query.filter(and_(buy_sell_flag='B', target_price=func.max(Instruction.target_price), stock_id=sto_id)).filter(Instruction.instruction_state.in_('N', 'P')).all()
        if len(buy) == 1:
            return buy
        else:
            earlybuy = Instruction()
            earlybuy.time = 999999
            for x in buy:
                if x.time < earlybuy.time:
                    earlybuy = x
            return earlybuy

    @staticmethod
    def getsellinstr(inst_id):
        temp = Instruction.query.get(inst_id)
        sto_id = temp.stock_id
        sell = Instruction.query.filter(and_(buy_sell_flag='S', target_price=func.min(Instruction.target_price), stock_id=sto_id)).filter(Instruction.instruction_state.in_('N', 'P')).all()
        if len(sell) == 1:
            return sell
        else:
            earlysell = Instruction()
            earlysell.time = 999999
            for x in sell:
                if x.time < earlysell.time:
                    earlysell = x
            return earlysell