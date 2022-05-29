from exts import db
from model.account_admin import AccountAdmin
from model.account_admin import Deal
from model.account_admin import PersonalSecuritiesAccount
from model.account_admin import LegalPersonSecuritiesAccount
from model.account_admin import FundAccount


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

    # 查找资金账户
    @staticmethod
    def get_fund(fund_account_number):
        fund_account = FundAccount.query.get(fund_account_number)
        return fund_account

    # 根据证券账户查找资金账户
    @staticmethod
    def get_fund_by_security(security_num):
        fund_account = FundAccount.query.filter_by(securities_account_number=security_num).first()
        return fund_account

    # 查找个人证券账户
    @staticmethod
    def get_personal(security_num):
        security_account = PersonalSecuritiesAccount.query.get(security_num)
        return security_account

    # 查找法人证券账户
    @staticmethod
    def get_legal(security_num):
        security_account = LegalPersonSecuritiesAccount.query.get(security_num)
        return security_account

    # 资金账户存款
    @staticmethod
    def fund_save_money(money, fund_account):
        fund_account.balance = fund_account.balance + money
        db.session.commit()

    # 资金账户取款
    @staticmethod
    def fund_take_money(money, fund_account):
        fund_account.balance = fund_account.balance - money
        db.session.commit()

    # 修改资金账户密码
    @staticmethod
    def fund_password(password, fund_account, trade_withdraw):
        if trade_withdraw == 0:
            fund_account.trade_password = password
        else:
            fund_account.login_password = password
        db.session.commit()

    # 资金账户删除一条记录（销户）
    @staticmethod
    def fund_delete_one(fund_account):
        print("start delete")
        db.session.delete(fund_account)
        print("delete ok")
        db.session.commit()

    # 证券账户冻结
    @staticmethod
    def security_froze(security_account):
        print("start froze")
        security_account.status = "no"
        print("froze ok")
        db.session.commit()

    # 根据个人身份证号查找证券账户
    @staticmethod
    def get_personal_by_id(id_num):
        security_account = PersonalSecuritiesAccount.query.get(id_num)
        return security_account
