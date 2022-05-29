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

class Stock(db.Model):
    __tablename__ = "stock"
    stock_id = db.Column(db.String(20), nullable=False, primary_key=True)
    stock_name = db.Column(db.String(20), nullable=False)
    remain_number = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Double, nullable=False)
    stock_type = db.Column(db.Char, nullable=False)
    stock_status = db.Column(db.Char, nullable=False)
    rise_threshold = db.Column(db.Double, nullable=False)
    fall_threshold = db.Column(db.Double, nullable=False)

class K(db.Model):
    __tablename__ = "k"
    k_id = db.Column(db.String(20), nullable=False, primary_key=True)
    stock_id = db.Column(db.String(20), db.ForeignKey("stock.stock_id"), nullable=False)
    start_price = db.Column(db.Double, nullable=True)
    end_price = db.Column(db.Double, nullable=True)
    highest_price = db.Column(db.Double, nullable=True)
    lowest_price = db.Column(db.Double, nullable=True)
    trade_number = db.Column(db.Integer, nullable=False)
    start_price = db.Column(db.Double, nullable=False)
    date = db.Column(db.Integer, nullable=False)

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