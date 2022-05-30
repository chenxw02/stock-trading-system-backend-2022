from exts import db


class Instruction(db.Model):
    __tablename__ = "instruction"
    instruction_id = db.Column(db.String(20), nullable = False, primary_key = True)
    stock_id = db.Column(db.String(20), db.ForeignKey("stock.stock_id"), nullable=False)
    fund_account_number = db.Column(db.String(20), db.ForeignKey("fund_account.fund_account_number"), nullable=False)
    buy_sell_flag = db.Column(db.Char, nullable=False)
    target_number = db.Column(db.Integer, nullable=False)
    actual_number = db.Column(db.Integer, nullable=False)
    target_price = db.Column(db.Double, nullable=False)
    time = db.Column(db.Integer(6), nullable=False)
    instruction_state = db.Column(db.Char, nullable=False)
    total_amount = db.Column(db.Double, nullable=False)

class Transaction(db.Model):
    __tablename__ = "transaction"
    transaction_id = db.Column(db.String(20), nullable=False, primary_key=True)
    stock_id = db.Column(db.String(20), db.ForeignKey("stock.stock_id"), nullable=False)
    instruction_id = db.Column(db.String(20), db.ForeignKey("instruction.instruction_id"), nullable=False)
    fund_account_number = db.Column(db.String(20), db.ForeignKey("fund_account.fund_account_number"), nullable=False)
    buy_sell_flag = db.Column(db.Char, nullable=False)
    transaction_price = db.Column(db.Double, nullable=False)
    transaction_amount = db.Column(db.Double, nullable=False)
    transaction_number = db.Column(db.Integer, nullable=False)
    transaction_date = db.Column(db.Integer, nullable=False)
    transaction_time= db.Column(db.Integer, nullable=False)