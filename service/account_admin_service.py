import jwt
import time
import bcrypt
from config import jwt_secret_key
from error.invalid_account import InvalidAccountError
from dao.account_admin_dao import AccountAdminDao
from model.account_admin import AccountAdmin
from model.account_admin import PersonalSecuritiesAccount
from model.account_admin import LegalPersonSecuritiesAccount


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
        password = account_information["password"].encode('utf-8')
        encrypted_password = bcrypt.hashpw(password, bcrypt.gensalt())
        account_information.append(PersonalSecuritiesAccount( \
            p_account_number=account_information["account_information"].encode('utf-8'), \
            password=encrypted_password, \
            user_name=account_information["user_name"].encode('utf-8'), \
            user_gender=account_information["user_gender"].encode('utf-8'), \
            registration_date=account_information["registration_date"], \
            user_id_number=account_information["user_id_number"].encode('utf-8'), \
            user_address=account_information["user_address"].encode('utf-8'), \
            user_job=account_information["user_job"].encode('utf-8'), \
            user_education=account_information["user_education"].encode('utf-8'), \
            user_work_unit=account_information["user_work_unit"].encode('utf-8'), \
            telephone=account_information["telephone"].encode('utf-8'), \
            agent=account_information["agent"], \
            agent_id=account_information["agent_id"].encode('utf-8'), \
            authority=account_information["authority"].encode('utf-8') \
            ))
        AccountAdminDao.insert(account_information)

    @staticmethod
    def add_legal_person_securities_account(account_data):
        account_information = []
        password = account_information["password"].encode('utf-8')
        encrypted_password = bcrypt.hashpw(password, bcrypt.gensalt())
        account_information.append(LegalPersonSecuritiesAccount( \
            l_account_number=account_information["l_account_number"].encode('utf-8'), \
            password=encrypted_password, \
            legal_person_registration_number=account_information["legal_person_registration_number"].encode('utf-8'), \
            business_license_number=account_information["business_license_number"].encode('utf-8'), \
            legal_person_id_number=account_information["legal_person_id_number"].encode('utf-8'), \
            legal_person_name=account_information["legal_person_name"].encode('utf-8'), \
            legal_person_telephone=account_information["legal_person_telephone"].encode('utf-8'), \
            legal_person_address=account_information["legal_person_address"].encode('utf-8'), \
            excutor=account_information["excutor"].encode('utf-8'), \
            authorized_person_id_number=account_information["authorized_person_id_number"].encode('utf-8'), \
            authorized_person_telephone=account_information["authorized_person_telephone"].encode('utf-8'), \
            authorized_person_address=account_information["authorized_person_address"].encode('utf-8'), \
            authority=account_information["authority"].encode('utf-8'), \
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
