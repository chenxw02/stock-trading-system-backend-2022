from exts import db


class Admin(db.Model):
    __tablename__ = "admin"
    admin_id = db.Column(db.String(20), nullable=False, primary_key=True)
    password = db.Column(db.String(200), nullable=False)