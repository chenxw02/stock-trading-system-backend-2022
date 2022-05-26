from exts import db
from model.account_admin import AccountAdmin
from model.account_admin import Deal
from model.account_admin import PersonalSecuritiesAccount
from model.account_admin import LegalPersonSecuritiesAccount

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

    # 如果该资金账户在证券账户中有对应，返回1，否则返回0
    @staticmethod
    def check_fund_account(securities_account_number):
        temp = PersonalSecuritiesAccount.query.get(securities_account_number)
        if temp != None:
            print("return 1-1")
            return 1
        temp = LegalPersonSecuritiesAccount.query.get(securities_account_number)
        if temp != None:
            print("return 1-2")
            return 1
        print("check_fund_account return 0")
        return 0
