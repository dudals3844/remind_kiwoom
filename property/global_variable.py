from PyQt5.QtCore import QEventLoop
from config.kiwoomType import RealType
from property.dataclass.account_base import AccountBase
from property.dataclass.hold_stock_base import HoldStockData
from property.dataclass.open_order_stock_base import StockOpenOrderData

TR_EVENTLOOP = QEventLoop()
ACCOUNT_DATA = AccountBase()
HOLD_STOCK = HoldStockData()
OPEN_ORDER_STOCK = StockOpenOrderData()
REAL_TYPE = RealType()


if __name__ == "__main__":
    pass