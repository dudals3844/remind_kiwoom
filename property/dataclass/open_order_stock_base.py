from dataclasses import dataclass, field
from typing import List


@dataclass
class StockOpenOrderBase:
    # 기업명
    name: str = None
    # 종목코드
    code: str = None
    # 주문상태 (접수, 체결, 확인)
    status: str = None
    # 주문수량
    order_quantity: int = None
    # 미체결 수량
    unfill_quantity: int = None
    # 주문가격
    price: float = None
    # 구분 (매수, 매도, 매수정정, 매도정정)
    gubun: str = None
    # 주문번호
    number: int = None
    # 원주문번호
    origin_number: str = None

@dataclass
class StockOpenOrderData:
    stock_open_order_list: List[StockOpenOrderBase] = field(default_factory=list)