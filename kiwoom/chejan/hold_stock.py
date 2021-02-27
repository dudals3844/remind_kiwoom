from property.dataclass.hold_stock_base import HoldStockBase
from property.global_variable import REAL_TYPE


class HoldStock:
    def receive(self) -> HoldStockBase:
        account_num = self.dynamicCall("GetChejanData(int)", REAL_TYPE.REALTYPE['잔고']['계좌번호'])
        code = self.dynamicCall("GetChejanData(int)", REAL_TYPE.REALTYPE['잔고']['종목코드'])[1:]

        stock_name = self.dynamicCall("GetChejanData(int)", REAL_TYPE.REALTYPE['잔고']['종목명'])
        stock_name = stock_name.strip()

        current_price = self.dynamicCall("GetChejanData(int)", REAL_TYPE.REALTYPE['잔고']['현재가'])
        current_price = abs(int(current_price))

        stock_quantity = self.dynamicCall("GetChejanData(int)", REAL_TYPE.REALTYPE['잔고']['보유수량'])
        stock_quantity = int(stock_quantity)

        like_quan = self.dynamicCall("GetChejanData(int)", REAL_TYPE.REALTYPE['잔고']['주문가능수량'])
        like_quan = int(like_quan)

        buy_price = self.dynamicCall("GetChejanData(int)", REAL_TYPE.REALTYPE['잔고']['매입단가'])
        buy_price = abs(int(buy_price))

        total_buy_price = self.dynamicCall("GetChejanData(int)",
                                           REAL_TYPE.REALTYPE['잔고']['총매입가'])  # 계좌에 있는 종목의 총매입가
        total_buy_price = int(total_buy_price)

        meme_gubun = self.dynamicCall("GetChejanData(int)", REAL_TYPE.REALTYPE['잔고']['매도매수구분'])
        meme_gubun = REAL_TYPE.REALTYPE['매도수구분'][meme_gubun]

        first_sell_price = self.dynamicCall("GetChejanData(int)", REAL_TYPE.REALTYPE['잔고']['(최우선)매도호가'])
        first_sell_price = abs(int(first_sell_price))

        first_buy_price = self.dynamicCall("GetChejanData(int)", REAL_TYPE.REALTYPE['잔고']['(최우선)매수호가'])
        first_buy_price = abs(int(first_buy_price))

        return HoldStockBase(
            name=stock_name,
            code=code,
            hold_quantity=stock_quantity,
            buy_price=buy_price,
            total_hold_price=total_buy_price
        )