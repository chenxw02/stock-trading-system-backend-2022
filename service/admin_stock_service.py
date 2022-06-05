from dao.admin_stock_dao import AdminStockDao


class AdminStockService:
    @staticmethod
    def get_permissions(admin_id):
        permissions = AdminStockDao.get_permissions(admin_id)
        return permissions

    @staticmethod
    def set_status(stock_id, stock_status):
        AdminStockDao.set_status(stock_id, stock_status)

    @staticmethod
    def set_threshold(stock_id, rise_threshold, fall_threshold):
        AdminStockDao.set_threshold(stock_id, rise_threshold, fall_threshold)

    @staticmethod
    def get_latest_transaction(stock_id):
        latest_transaction = AdminStockDao.get_latest_transaction(stock_id)
        if latest_transaction is None:
            return None
        return {
            "latest_amount": latest_transaction.transaction_number,
            "latest_price": latest_transaction.transaction_price
        }

    @staticmethod
    def get_instructions(buy_or_sell, stock_id):
        result = []
        instructions = AdminStockDao.get_instructions(buy_or_sell, stock_id)
        for instruction in instructions:
            result.append({
                "instruction_id": instruction.instruction_id,
                "stock_id": instruction.stock_id,
                "fund_account_number": instruction.fund_account_number,
                "buy_sell_flag": instruction.buy_sell_flag,
                "target_number": instruction.target_number,
                "actual_number": instruction.actual_number,
                "target_price": instruction.target_price,
                "time": instruction.time,
                "instruction_state": instruction.instruction_state,
                "total_amount": instruction.total_amount
            })
        return result
