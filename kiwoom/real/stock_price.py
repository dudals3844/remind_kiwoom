from property.global_variable import REAL_TYPE
from property.enum.screen_number_enum import ScreenNumberEnum
from property.dataclass.real_stock_price_dataclass import RealStockPriceDataclass



class StockPrice:
    def request(self, code):
        fids = REAL_TYPE.REALTYPE['주식체결']['체결시간']
        self.dynanicCall("SetRealReg(QString, QString, QString, QString)", ScreenNumberEnum.REAL_STOCK_DATA.value, code,
                         fids,
                         "1")

    def receive(self, sCode, sRealType) -> RealStockPriceDataclass:
        time = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                REAL_TYPE.REALTYPE[sRealType]['체결시간'])  # 출력 HHMMSS
        now_price = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                     REAL_TYPE.REALTYPE[sRealType]['현재가'])  # 출력 : +(-)2520
        now_price = abs(int(now_price))

        yesterday_diff = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                          REAL_TYPE.REALTYPE[sRealType]['전일대비'])  # 출력 : +(-)2520
        yesterday_diff = abs(int(yesterday_diff))

        yesterday_diff_percent = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                  REAL_TYPE.REALTYPE[sRealType]['등락율'])  # 출력 : +(-)12.98
        yesterday_diff_percent = float(yesterday_diff_percent)

        medo_1_hoga = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                       REAL_TYPE.REALTYPE[sRealType]['(최우선)매도호가'])  # 출력 : +(-)2520
        medo_1_hoga = abs(int(medo_1_hoga))

        mesu_1_hoga = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                       REAL_TYPE.REALTYPE[sRealType]['(최우선)매수호가'])  # 출력 : +(-)2515
        mesu_1_hoga = abs(int(mesu_1_hoga))

        volume = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                  REAL_TYPE.REALTYPE[sRealType]['거래량'])  # 출력 : +240124 매수일때, -2034 매도일 때
        volume = abs(int(volume))

        volume_sum = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                      REAL_TYPE.REALTYPE[sRealType]['누적거래량'])  # 출력 : 240124
        volume_sum = abs(int(volume_sum))

        high_price = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                      REAL_TYPE.REALTYPE[sRealType]['고가'])  # 출력 : +(-)2530
        high_price = abs(int(high_price))

        start_price = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                       REAL_TYPE.REALTYPE[sRealType]['시가'])  # 출력 : +(-)2530
        start_price = abs(int(start_price))

        low_price = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                     REAL_TYPE.REALTYPE[sRealType]['저가'])  # 출력 : +(-)2530
        low_price = abs(int(low_price))

        return RealStockPriceDataclass(
            code=sCode,
            time=time,
            now_price=now_price,
            yesterday_diff=yesterday_diff,
            yesterday_diff_percent=yesterday_diff_percent,
            medo_1_hoga=medo_1_hoga,
            mesu_1_hoga=mesu_1_hoga,
            volume=volume,
            volume_sum=volume_sum,
            high_price=high_price,
            low_price=low_price
        )


    def disconnect_stock_price(self, code):
        self.dynamicCall("SetRealRemove(QString, QString)", ScreenNumberEnum.REAL_STOCK_DATA.value, code)
