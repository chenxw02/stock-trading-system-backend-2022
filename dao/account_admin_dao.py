from exts import db
from model.account_admin import AccountAdmin
from model.account_admin import Deal

# 将一个表的所有简单操作集中成一个dao数据库类
class AccountAdminDao:
    @staticmethod
    def insert(account_admins):
        db.session.add_all(account_admins)
        db.session.commit()

    @staticmethod
    def get(administrator_id):
        account_admin = AccountAdmin.query.get(administrator_id)
        return account_admin

    @staticmethod
    def get_deals():
        deals = Deal.query.all()
        return deals
