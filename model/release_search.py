from exts import db

class TestTransaction(db.Model):
    _tablename_ = "test_transaction"
    transaction_id = db.Column(db.String(20), nullable=False, primary_key=True)
    stock_id = db.Column(db.String(20), db.ForeignKey("stock.stock_id"), nullable=False)
    instruction_id = db.Column(db.String(20), nullable=False)
    fund_account_id = db.Column(db.String(20), nullable=False)
    buy_sell_flag = db.Column(db.CHAR, nullable=False)
    transaction_price = db.Column(db.Float, nullable=False)
    transaction_amount = db.Column(db.Float, nullable=False)
    transaction_number = db.Column(db.Integer, nullable=False)
    transaction_date = db.Column(db.Integer, nullable=False)
    transaction_time = db.Column(db.Integer, nullable=False)

    
