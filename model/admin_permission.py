from exts import db
from sqlalchemy import ForeignKey


class AdminPermission(db.Model):
    __tablename__ = "admin_permission"
    admin_id = db.Column(db.String(20), ForeignKey('admin.admin_id'), nullable=False, primary_key=True)
    stock_id = db.Column(db.String(20), ForeignKey('stock.stock_id'), nullable=False, primary_key=True)
