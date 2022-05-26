import jwt
import time
import bcrypt
from config import jwt_secret_key
from error.invalid_account import InvalidAccountError
from dao.account_admin_dao import AccountAdminDao
from model.account_admin import AccountAdmin
from model.account_admin import PersonalSecuritiesAccount
from model.account_admin import LegalPersonSecuritiesAccount
from model.account_admin import FundAccount
from model.account_admin import OwnStock


class AccountAdminService:
    @staticmethod
    def login(administrator_id, administrator_password):
        account_admin = AccountAdminDao.get(administrator_id)
        if account_admin is None:
            raise InvalidAccountError()
        encrypted_password = account_admin.administrator_password
        if not bcrypt.checkpw(administrator_password.encode("utf-8"), encrypted_password.encode("utf-8")):
            raise InvalidAccountError()
            # raise 以返回账号密码错误
        headers = {
            "alg": "HS256",
            "typ": "JWT"
        }
        # 设置超时时间：当前时间的30分钟以后超时
        exp = int(time.time() + 60 * 30)
        payload = {
            "administrator_id": administrator_id,
            "type": "account_admin",
            "exp": exp
        }
        token = jwt.encode(payload=payload, key=jwt_secret_key, algorithm='HS256', headers=headers)
        return token

    @staticmethod
    def show_deal():
        result = {}
        temp_deal = AccountAdminDao.get_deals()
        for temp in temp_deal:
            result[temp.deal_id] = temp.status
        print("dxp:")
        print(result)
        return result

    @staticmethod
    def add_personal_securities_account(account_data):
        account_information = []
        print(account_data)
        password = account_data["password"].encode('utf-8')
        encrypted_password = bcrypt.hashpw(password, bcrypt.gensalt())
        account_information.append(PersonalSecuritiesAccount( \
            p_account_number=account_data["p_account_number"].encode('utf-8'), \
            password=encrypted_password, \
            user_name=account_data["user_name"].encode('utf-8'), \
            user_gender=account_data["user_gender"].encode('utf-8'), \
            registration_date=account_data["registration_date"], \
            user_id_number=account_data["user_id_number"].encode('utf-8'), \
            user_address=account_data["user_address"].encode('utf-8'), \
            user_job=account_data["user_job"].encode('utf-8'), \
            user_education=account_data["user_education"].encode('utf-8'), \
            user_work_unit=account_data["user_work_unit"].encode('utf-8'), \
            telephone=account_data["telephone"].encode('utf-8'), \
            agent=account_data["agent"], \
            agent_id=account_data["agent_id"].encode('utf-8'), \
            authority=account_data["authority"].encode('utf-8') ))
        print(account_information)
        AccountAdminDao.insert(account_information)

    @staticmethod
    def add_legal_person_securities_account(account_data):
        account_information = []
        password = account_data["password"].encode('utf-8')
        encrypted_password = bcrypt.hashpw(password, bcrypt.gensalt())
        account_information.append(LegalPersonSecuritiesAccount( \
            l_account_number=account_information["l_account_number"].encode('utf-8'), \
            password=encrypted_password, \
            legal_person_registration_number=account_data["legal_person_registration_number"].encode('utf-8'), \
            business_license_number=account_data["business_license_number"].encode('utf-8'), \
            legal_person_id_number=account_data["legal_person_id_number"].encode('utf-8'), \
            legal_person_name=account_data["legal_person_name"].encode('utf-8'), \
            legal_person_telephone=account_data["legal_person_telephone"].encode('utf-8'), \
            legal_person_address=account_data["legal_person_address"].encode('utf-8'), \
            excutor=account_data["excutor"].encode('utf-8'), \
            authorized_person_id_number=account_data["authorized_person_id_number"].encode('utf-8'), \
            authorized_person_telephone=account_data["authorized_person_telephone"].encode('utf-8'), \
            authorized_person_address=account_data["authorized_person_address"].encode('utf-8'), \
            authority=account_data["authority"].encode('utf-8') \
            ))
        AccountAdminDao.insert(account_information)

    # 实际并没有这个接口开放，可以事先开放插入管理员之后关闭它
    @staticmethod
    def register(admins_data):
        account_admins = []
        password = admins_data["administrator_password"].encode('utf-8')
        print(password)
        encrypted_password = bcrypt.hashpw(password, bcrypt.gensalt())
        print(encrypted_password)
        account_admins.append(
            AccountAdmin(administrator_id=admins_data["administrator_id"], administrator_password=encrypted_password))
        AccountAdminDao.insert(account_admins)

    # 添加一个资金账户，合法返回1，否则返回0
    @staticmethod
    def add_fund_account(fund_account_data):
        account_information = []
        securities_account_number = fund_account_data["securities_account_number"]
        print(securities_account_number)
        if (AccountAdminDao.check_fund_account(securities_account_number) == 0):
            return "failed"
        trade_password = fund_account_data["trade_password"].encode('utf-8')
        encrypted_trade_password = bcrypt.hashpw(trade_password, bcrypt.gensalt())
        login_password = fund_account_data["login_password"].encode('utf-8')
        encrypted_login_password = bcrypt.hashpw(login_password, bcrypt.gensalt())
        account_information.append(FundAccount(fund_account_number=fund_account_data["fund_account_number"],
                                               balance=fund_account_data["balance"], frozen=fund_account_data["frozen"],
                                               taken=fund_account_data["taken"],
                                               trade_password=encrypted_trade_password,
                                               login_password=encrypted_login_password,
                                               account_status=fund_account_data["account_status"],
                                               securities_account_number=fund_account_data["securities_account_number"]))
        AccountAdminDao.insert(account_information)
        print(account_information)
        return "ok"

