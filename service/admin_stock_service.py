from dao.admin_stock_dao import AdminStockDao


class AdminStockService:
    @staticmethod
    def get_permissions(admin_id):
        permissions = AdminStockDao.get_permissions(admin_id)
        return permissions

    @staticmethod
    def set_status(stock_id, stock_status):
        AdminStockDao.set_status(stock_id, stock_status)

    @staticmethod
    def set_threshold(stock_id, rise_threshold, fall_threshold):
        AdminStockDao.set_threshold(stock_id, rise_threshold, fall_threshold)

    @staticmethod
    def get_latest_transaction(stock_id):
        latest_transaction = AdminStockDao.get_latest_transaction(stock_id)
        return {
            "latest_amount": latest_transaction.transaction_number,
            "latest_price": latest_transaction.transaction_price
        }
