from dataclasses import dataclass



@dataclass
class StockData:
    name: str = None
    code: str = None
    hold_quantity: int = None
    buy_price: float = None
    total_hold_price: float = None
    profit: float = None


