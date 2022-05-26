from dao.con_auc_dao import ConAucDao
from model.con_auc import Instruction

class ConAucService:



    #连续竞价
    @staticmethod
    def continue_auction():
        buy = ConAucDao.getbuyinstr()
        sell = ConAucDao.getsellinstr()
        if buy.target_price < sell.target_price:
            return 0    ##无法交易标志，没想好
        else:
            transaction_price = 0.5 * (buy.target_price * sell.target_price)
            buyrest = buy.target_number - buy.actual_number
            sellrest = sell.target_number - sell.actual_number
            transaction_number = min(buyrest, sellrest)
            tup = [buy.instruction_id, sell.instruction_id, transaction_price, transaction_number]
            return tup

