import jwt
import time
from config import jwt_secret_key

def login(admin_id, password):
    # print(admin_id)
    # print(password)
    # TODO:从数据库核验是否正确,如果不正确抛出异常/直接返回空
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