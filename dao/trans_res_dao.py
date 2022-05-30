from exts import db
from model.trans_res import Instruction
from model.trans_res import Transaction


class TransResDao:

    # 获取股票编号
    @staticmethod
    def gettransstock(instr_id):
        instr = Instruction.query.filter(Instruction.stock_id == instr_id)
        return instr.stock_id

    # 获取买卖标志
    @staticmethod
    def gettransflag(instr_id):
        instr = Instruction.query.filter(Instruction.stock_id == instr_id)
        return instr.buy_sell_flag

    # 获取账户编号
    @staticmethod
    def gettransaccount(instr_id):
        instr = Instruction.query.filter(Instruction.stock_id == instr_id)
        return instr.fund_account_number

    # 获取指令编号
    @staticmethod
    def gettransinstr(instr_id):
        instr = Instruction.query.filter(Instruction.stock_id == instr_id)
        return instr.instruction_id

    # 生成交易结果
    @staticmethod
    def updatetransinfo(s_id, b_s_flag, a_number, t_price, t_amount, t_number, t_date, t_time, i_id):
        trans = Transaction()
        trans.stock_id = s_id
        trans.buy_sell_flag = b_s_flag
        trans.fund_account_number = a_number
        trans.transaction_price = t_price
        trans.transaction_amount = t_amount
        trans.transaction_number = t_number
        trans.transaction_date = t_date
        trans.transaction_time = t_time
        trans.instruction_id = i_id
        db.session.add(trans)
        db.session.commit()
        return trans.transaction_id
