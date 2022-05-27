from exts import db
from model.query_user import QueryUser

# 将一个表的所有简单操作集中成一个dao数据库类
class QueryUserDao:
    @staticmethod
    def insert(query_user):
        db.session.add_all(query_user)
        db.session.commit()

    @staticmethod
    def get(query_user_id):
            query_user = QueryUser.query.get(query_user_id)
            return query_user


    @staticmethod
    def update(query_user):
        db.session.add(query_user)
        db.session.commit()

