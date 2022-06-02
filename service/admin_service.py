import jwt
import time
import bcrypt
from config import jwt_secret_key
from error.invalid_account import InvalidAccountError
from dao.admin_dao import AdminDao
from model.admin import Admin


class AdminService:
    @staticmethod
    def login(admin_id, password):
        admin = AdminDao.get(admin_id)
        if admin is None:
            raise InvalidAccountError()
        encrypted_password = admin.password
        if not bcrypt.checkpw(password.encode("utf-8"), encrypted_password.encode("utf-8")):
            raise InvalidAccountError()
            # raise 以返回账号密码错误
        headers = {
            "alg": "HS256",
            "typ": "JWT"
        }
        # 设置超时时间：当前时间的30分钟以后超时
        exp = int(time.time() + 60*30)
        payload = {
            "admin_id": admin_id,
            "type": "admin",
            "exp": exp
        }
        token = jwt.encode(payload=payload, key=jwt_secret_key, algorithm='HS256', headers=headers)
        return token

    # 实际并没有这个接口开放，可以事先开放插入管理员之后关闭它
    @staticmethod
    def register(admins_data):
        admins = []
        for admin_data in admins_data:
            password = admin_data["password"].encode('utf-8')
            encrypted_password = bcrypt.hashpw(password, bcrypt.gensalt())
            # print(encrypted_password)
            admins.append(Admin(admin_id=admin_data["admin_id"], password=encrypted_password))
        AdminDao.insert(admins)

    @staticmethod
    def change_password(admin_id, password, new_password):
        # print(admin_id)
        # print(password)
        # print(new_password)
        admin = AdminDao.get(admin_id)
        if admin is None:
            raise InvalidAccountError()
        encrypted_password = admin.password
        if not bcrypt.checkpw(str(password).encode("utf-8"), encrypted_password.encode("utf-8")):
            raise InvalidAccountError()
        # 原密码正确，则继续修改密码
        new_encrypted_password = bcrypt.hashpw(str(new_password).encode('utf-8'), bcrypt.gensalt())
        AdminDao.update(admin_id, new_encrypted_password)

    @staticmethod
    def get_permissions(admin_id):
        permissions = AdminDao.get_permissions(admin_id)
        return permissions

    @staticmethod
    def set_status(stock_id, stock_status):
        AdminDao.set_status(stock_id, stock_status)
