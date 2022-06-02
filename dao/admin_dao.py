from exts import db
from model.admin import Admin
from model.admin_permission import AdminPermission
from model.center_trade import Stock


# 将一个表的所有简单操作集中成一个dao数据库类
class AdminDao:
    @staticmethod
    def insert(admins):
        db.session.add_all(admins)
        db.session.commit()

    @staticmethod
    def get(admin_id):
        admin = Admin.query.get(admin_id)
        return admin

    @staticmethod
    def update(admin_id, new_password):
        admin = Admin.query.get(admin_id)
        admin.password = new_password
        db.session.commit()

    @staticmethod
    def get_permissions(admin_id):
        result = []
        for permission, stock in db.session.query(AdminPermission, Stock).filter(Stock.stock_id == AdminPermission.stock_id and AdminPermission.admin_id == admin_id).all():
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
