from exts import db
from model.admin import Admin
from model.admin_permission import AdminPermission
from model.center_trade import Stock
from model.center_trade import Transaction
from sqlalchemy import func


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

    @staticmethod
    def set_threshold(stock_id, rise_threshold, fall_threshold):
        stock = Stock.query.get(stock_id)
        stock.rise_threshold = rise_threshold
        stock.fall_threshold = fall_threshold
        db.session.commit()

    @staticmethod
    def get_latest_transaction(stock_id):
        latest_row = db.session.query(func.max(Transaction.transaction_timestamp).label("latest_time")).filter(Transaction.stock_id == stock_id).one()
        latest_time = latest_row.latest_time
        latest_transaction = Transaction.query.filter_by(transaction_timestamp=latest_time).first()
        return latest_transaction

