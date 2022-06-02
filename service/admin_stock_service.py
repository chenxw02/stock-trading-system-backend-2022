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
