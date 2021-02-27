from dataclasses import dataclass, field
from typing import List


@dataclass
class HoldStockBase:
    name: str = None
    code: str = None
    hold_quantity: int = None
    buy_price: float = None
    total_hold_price: float = None


# https://www.daleseo.com/python-dataclasses/ 참
@dataclass
class HoldStockData:
    hold_stock_list: List[HoldStockBase] = field(default_factory=list)

    def is_in_list(self, code):
        is_in_list = list(filter(lambda x: x.code == code, self.hold_stock_list))
        if len(is_in_list) == 0:
            return False
        else:
            return True



