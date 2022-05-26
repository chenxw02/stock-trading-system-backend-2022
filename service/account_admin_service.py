import jwt
import time
import bcrypt
from config import jwt_secret_key
from error.invalid_account import InvalidAccountError
from dao.account_admin_dao import AccountAdminDao
from model.account_admin import AccountAdmin


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

 #   @staticmethod
 #   def deal(administrator_id, administrator_password):