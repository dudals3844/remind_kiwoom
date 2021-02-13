from dataclasses import dataclass


@dataclass
class StockOpenOrderData:
    name: str = None
    code: str = None
    status: str = None
    total_order_quantity: int = None
    quantity: int = None
    price: float = None
    number: str = None
    origin_number: str = None
