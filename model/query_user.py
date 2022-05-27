from exts import db


class QueryUser(db.Model):
    __tablename__ = "queryuser"
    ID = db.Column(db.String(20), nullable=False, primary_key=True)
    password = db.Column(db.String(200), nullable=False)
    authority = db.Column(db.CHAR, nullable=False)

class PayAccount(db.Model):
    __tablename__ = "payaccount"
    pay_account_id = db.Column(db.String(20), nullable=False, primary_key=True)
    pay_account_psw = db.Column(db.String(200), nullable=False)
    balance =  db.Column(db.INT, nullable=False)
