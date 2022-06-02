from exts import db
from model.admin import Admin
from model.admin_permission import AdminPermission
from model.center_trade import Stock


class AdminStockDao:
    @staticmethod
    def get_permissions(admin_id):
        result = []
        for permission, stock in db.session.query(AdminPermission, Stock).filter(
                Stock.stock_id == AdminPermission.stock_id and AdminPermission.admin_id == admin_id).all():
            result.append({
                "stock_id": stock.stock_id,
                "stock_name": stock.stock_name,
                "status": stock.stock_status
            })
        # print(result)
        return result

    @staticmethod
    def set_status(stock_id, stock_status):
        stock = Stock.query.get(stock_id)
        stock.stock_status = stock_status
        db.session.commit()
