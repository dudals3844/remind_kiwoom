from dataclasses import dataclass



@dataclass
class Stock:
    name: str = None
    code: str = None
    hold_number: int = None
    buy_price: float = None
    total_hold_price: float = None
    profit: float = None


