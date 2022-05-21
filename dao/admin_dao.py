from exts import db
from admin import Admin

# 将一个表的所有简单操作集中成一个dao数据库类
class AdminDao:
    @staticmethod
    def insert(admins):
        db.session.add_all(admins)
        db.session.commit()

    @staticmethod
    def get(admin_id):
        admin = Admin.query.get(admin_id)
        return admin
