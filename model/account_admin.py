from exts import db


class AccountAdmin(db.Model):
    __tablename__ = "administrator_account"
    administrator_id = db.Column(db.String(20), nullable=False, primary_key=True)
    administrator_password = db.Column(db.String(200), nullable=False)