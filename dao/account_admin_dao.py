from exts import db
from model.account_admin import AccountAdmin
from model.account_admin import Deal
from model.account_admin import PersonalSecuritiesAccount
from model.account_admin import LegalPersonSecuritiesAccount
from model.account_admin import FundAccount
from sqlalchemy import text
from sqlalchemy import func


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
    # 检查该证券账户是否已经有对应的资金账户
    @staticmethod
    def check_securities_account(securities_account_number):
        temp = FundAccount.query.filter_by(securities_account_number=securities_account_number).first()
        print(temp)
        if temp is not None:
            return 0
        return 1



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
        security_account.status = "no"
        db.session.commit()

    # 证券账户解冻
    @staticmethod
    def security_thaw(security_account):
        security_account.status = "ok"
        db.session.commit()

    # 资金账户冻结
    @staticmethod
    def fund_froze(fund_account):
        fund_account.account_status = "no"
        db.session.commit()

    # 资金账户解冻
    @staticmethod
    def fund_thaw(fund_account):
        fund_account.account_status = "ok"
        db.session.commit()

    # 根据个人身份证号查找证券账户
    @staticmethod
    def get_personal_by_id(id_num):
        security_account = PersonalSecuritiesAccount.query.filter_by(user_id_number=id_num).first()
        return security_account

    # 根据法人注册登记号查找证券账户
    @staticmethod
    def get_legal_person_by_id(legal_register_num):
        security_account = LegalPersonSecuritiesAccount.query.filter_by(
            legal_person_registration_number=legal_register_num).first()
        return security_account

    @staticmethod
    def re_add_personal_securities_account(old_class, new_password, new_p_number):
        old_class.password = new_password
        old_class.p_account_number = new_p_number
        old_class.status = "ok"
        db.session.commit()

    @staticmethod
    def re_add_legal_person_securities_account(old_class, new_password, new_l_number):
        old_class.password = new_password
        old_class.l_account_number = new_l_number
        old_class.status = "ok"
        db.session.commit()

    @staticmethod
    def re_add_fund_account(old_class, new_login_password, new_trade_password, new_number):
        old_class.login_password = new_login_password
        old_class.trade_password = new_trade_password
        old_class.fund_account_number = new_number
        old_class.account_status = "ok"
        db.session.commit()

    # 根据证券帐号查找资金账户
    @staticmethod
    def get_fund_by_securities_account(securities_account_number):
        fund_account = FundAccount.query.filter_by(securities_account_number=securities_account_number).first()
        return fund_account

    # 个人证券账户删除一条记录（销户）
    @staticmethod
    def personal_delete_one(fund_account):
        print("start delete")
        db.session.delete(fund_account)
        print("delete ok")
        db.session.commit()

    # 法人证券账户删除一条记录（销户）
    @staticmethod
    def legal_personal_delete_one(fund_account):
        print("start delete")
        db.session.delete(fund_account)
        print("delete ok")
        db.session.commit()

    @staticmethod
    def get_securities_account_information_by_query(sql_query, account_data):
        print(sql_query)
        p_account_number = "p_" + account_data["p_account_number"]
        user_id_number = account_data["user_id_number"]
        user_name = account_data["user_name"]
        status = account_data["status"]
        agent = account_data["agent"]
        user_address = account_data["user_address"]
        print(user_address)
        security_account = PersonalSecuritiesAccount.query.filter(text(sql_query)).params(
            p_account_number=p_account_number, user_id_number=user_id_number, user_name=user_name, status=status,
            agent=agent, user_address=user_address).all()
        return security_account

    @staticmethod
    def get_fund_account_information_by_query(sql_query, account_data):
        print(sql_query)
        fund_account_number = account_data["fund_account_number"]
        securities_account_number = account_data["securities_account_number"]
        status = account_data["status"]
        balance = account_data["balance"]
        label = account_data["label"]
        if label == "0":
            securities_account_number = "l_"+securities_account_number
        else:
            securities_account_number = "p_"+securities_account_number
        fund_account = FundAccount.query.filter(text(sql_query)).params(
            fund_account_number=fund_account_number, securities_account_number=securities_account_number, status=status,
            balance=balance).all()
        return fund_account

    @staticmethod
    def get_deal_id():
        new_id = db.session.query(func.max(Deal.deal_id)).first()[0] + 1
        return new_id

    @staticmethod
    def handle_deal(id, ifapproval):
        deal = Deal.query.get(id)
        print(deal)
        securities_account_number = deal.securities_account_number
        id_num = deal.person_id
        print(id_num)
        if securities_account_number[0] == 'p':
            temp = PersonalSecuritiesAccount.query.filter_by(user_id_number=id_num).first()
            if temp is None:
                return -1
            if temp.p_account_number != securities_account_number:
                return 0
        else:
            temp = LegalPersonSecuritiesAccount.query.filter_by(legal_person_registration_number = id_num).first()
            if temp is None:
                return -1
            if temp.l_account_number != securities_account_number:
                return 0
        deal.status = ifapproval
        db.session.commit()
        return 1
