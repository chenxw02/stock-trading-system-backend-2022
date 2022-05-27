from exts import db
from model.query_user import PayAccount

# 将一个表的所有简单操作集中成一个dao数据库类
class PaymentDao:
    @staticmethod
    def insert(pay_accpunt):
        db.session.add_all(pay_accpunt)
        db.session.commit()

    @staticmethod
    def get(pay_account_id):
            pay_accpunt = PayAccount.query.get(pay_account_id)
            return pay_accpunt

    @staticmethod
    def update(pay_accpunt):
        db.session.add(pay_accpunt)
        db.session.commit()
