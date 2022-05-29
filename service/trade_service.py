from dao.trade_dao import TradeDao


class TradeService:
    @staticmethod
    def show_fund_info(fund_acc_num):
        data = TradeDao.get_fund_info(fund_acc_num)
        # if data is None:
        #     raise
        return data
    
    @staticmethod
    def show_own_stock_info(fund_acc_num):
        data = TradeDao.get_own_stock_info(fund_acc_num)
        # if data is None:
        #     raise
        return data

    @staticmethod
    def update_buy(trans_id):
        data = TradeDao.update_fund_acc(trans_id)
        # if data is None:
        #     raise
        return data

    @staticmethod
    def update_sell(trans_id):
        data = TradeDao.update_own_stock(trans_id)
        # if data is None:
        #     raise
        return data