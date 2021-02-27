from kiwoom.trading import Trading
from kiwoom.real.stock_market_check import StockMarketCheck
from property.enum.stock_market_check_enum import StockMarketEnum


class UpperLimitBreakthrough(Trading):
    def __init__(self):
        super().__init__()
        StockMarketCheck.request(self)

    def realdata_slot(self, sCode, sRealType, sRealData):
        if sRealType == '장시작시간':
            status = StockMarketCheck.receive(self, sCode, sRealType)
            if status == StockMarketEnum.BEFORE_START.value:
                pass
            elif status == StockMarketEnum.START.value:
                pass
            elif status == StockMarketEnum.SINGLE_PRICE_AUCTION_CALL.value:
                pass
            elif status == StockMarketEnum.END.value:
                pass
            else:
                raise Exception("StockMarketCheck Error")




    def chejan_slot(self, sGubun, nItemCnt, sFidList):
        pass


