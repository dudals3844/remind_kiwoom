from dataclasses import dataclass



@dataclass
class StockData:
    name: str = None
    code: str = None
    hold_quantity: int = None
    buy_price: float = None
    total_hold_price: float = None
    profit: float = None


    @staticmethod
    def is_in_list(code):
        is_in_list = list(filter(lambda x: x.code == code, HOLD_STOCK_LIST))
        if len(is_in_list) == 0:
            return False
        else:
            return True


