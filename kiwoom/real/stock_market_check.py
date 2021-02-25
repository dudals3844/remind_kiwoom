from property.screen_number_enum import ScreenNumberEnum
from property.stock_market_check_enum import StockMarketEnum
from property.global_variable import REAL_TYPE

class StockMarketCheck:
    def request(self):
        self.dynamicCall("SetRealReg(QString, QString, QString, QString)", ScreenNumberEnum.START_STOP_REAL.value, '',
                         REAL_TYPE.REALTYPE['장시작시간']['장운영구분'], "0")

    def receive(self, sCode, sRealType):
        fid = REAL_TYPE.REALTYPE[sRealType]['장운영구분']
        value = self.dynamicCall("GetCommRealData(QString, int)", sCode, fid)
        if value == '0':
            print('장 시작전')
            return StockMarketEnum.BEFORE_START.value
        elif value == '3':
            print('장 시작')
            return StockMarketEnum.START.value
        elif value == '2':
            print('장 종료: 동시호가로 넘어감')
            return StockMarketEnum.SINGLE_PRICE_AUCTION_CALL.value
        elif value == '4':
            print('3시 30분 장 종')
            return StockMarketEnum.END.value
        else:
            raise Exception("Stock Market Check Error")