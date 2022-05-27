import jwt
import time
import bcrypt


from config import jwt_secret_key
from error.invalid_account import InvalidAccountError,InvalidAccountNameError,NoneAccountNameError,InvalidPaymentAccountError,LackOfBalance,AlreadyAdvance
from dao.query_user_dao import QueryUserDao
from model.query_user import QueryUser
from dao.payment_dao import PaymentDao
from unit.result import Result
prefix = "40"

class QueryUserService:
    @staticmethod
    def login(query_user_id,query_user_psw):
        query_user = QueryUserDao.get(query_user_id)
        if query_user is None:
            raise InvalidAccountError()
        encrypted_password = query_user.password
        if not bcrypt.checkpw(query_user_psw.encode("utf-8"), encrypted_password.encode("utf-8")):
            raise InvalidAccountError()
        #  返回“账号或密码错误

        headers = {
            "alg": "HS256",
            "typ": "JWT"
        }
        Authority = query_user.authority
        # 设置超时时间：当前时间的30分钟以后超时
        exp = int(time.time() + 60 * 30)
        payload = {
            "query_user_id": query_user_id,
            "type": Authority,
            "exp": exp
        }
        token = jwt.encode(payload=payload, key=jwt_secret_key, algorithm='HS256', headers=headers)
        returning = {
            "token": token,
            "type": Authority,
            "query_user_id": query_user_id
        }

        return returning



    @staticmethod
    def register(query_user_data):
        query_user = []
        password = query_user_data["password"].encode('utf-8')
        encrypted_password = bcrypt.hashpw(password, bcrypt.gensalt())
        Authority = "P"
        Payment = 0
        ID = query_user_data["ID"]
        query_user_temp = QueryUserDao.get(ID)
        if query_user_temp is not None:
            raise InvalidAccountNameError()
        query_user.append(QueryUser(ID=ID, password=encrypted_password,authority=Authority))
        QueryUserDao.insert(query_user)

    @staticmethod
    def modify(query_user_data):
        ID = query_user_data["ID"]
        query_user_temp = QueryUserDao.get(ID)
        if query_user_temp is None:
            raise NoneAccountNameError()
        password = query_user_data["password"].encode('utf-8')
        encrypted_password = bcrypt.hashpw(password, bcrypt.gensalt())
        query_user_temp.password = encrypted_password
        QueryUserDao.update(query_user_temp)

    @staticmethod
    def upgrade(upgrade_data):
        ID = upgrade_data["ID"]
        upgrade_user_temp = QueryUserDao.get(ID)
        if upgrade_user_temp is None:
            raise NoneAccountNameError()
        pay_account_id = upgrade_data["pay_account_id"]
        pay_account_tmp = PaymentDao.get(pay_account_id)
        if pay_account_tmp is None:
            raise InvalidPaymentAccountError()
        pay_password = pay_account_tmp.pay_account_psw
        if pay_password != upgrade_data["pay_account_psw"]:
            raise InvalidPaymentAccountError()
        if upgrade_user_temp.authority == "H":
            raise AlreadyAdvance()
        upgrade_user_temp.authority = "H"
        QueryUserDao.update(upgrade_user_temp)
        if pay_account_tmp.balance < 50:
            raise LackOfBalance()
        pay_account_tmp.balance -= 50
        PaymentDao.update(pay_account_tmp)









