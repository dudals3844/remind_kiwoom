from property.dataclass.open_order_stock_base import StockOpenOrderBase
from property.global_variable import REAL_TYPE

class OpenOrder:
    def receive(self) -> StockOpenOrderBase:
        account_num = self.dynamicCall("GetChejanData(int)", REAL_TYPE.REALTYPE['주문체결']['계좌번호'])
        sCode = self.dynamicCall("GetChejanData(int)", REAL_TYPE.REALTYPE['주문체결']['종목코드'])[1:]
        stock_name = self.dynamicCall("GetChejanData(int)", REAL_TYPE.REALTYPE['주문체결']['종목명'])
        stock_name = stock_name.strip()

        origin_order_number = self.dynamicCall("GetChejanData(int)",
                                               REAL_TYPE.REALTYPE['주문체결']['원주문번호'])  # 출력 : defaluse : "000000"
        order_number = self.dynamicCall("GetChejanData(int)",
                                        REAL_TYPE.REALTYPE['주문체결']['주문번호'])  # 출럭: 0115061 마지막 주문번호

        order_status = self.dynamicCall("GetChejanData(int)",
                                        REAL_TYPE.REALTYPE['주문체결']['주문상태'])  # 출력: 접수, 확인, 체결
        order_quantity = self.dynamicCall("GetChejanData(int)", REAL_TYPE.REALTYPE['주문체결']['주문수량'])  # 출력 : 3
        order_quantity = int(order_quantity)

        order_price = self.dynamicCall("GetChejanData(int)", REAL_TYPE.REALTYPE['주문체결']['주문가격'])  # 출력: 21000
        order_price = int(order_price)

        unfill_quantity = self.dynamicCall("GetChejanData(int)",
                                            REAL_TYPE.REALTYPE['주문체결']['미체결수량'])  # 출력: 15, default: 0
        unfill_quantity = int(unfill_quantity)

        order_gubun = self.dynamicCall("GetChejanData(int)", REAL_TYPE.REALTYPE['주문체결']['주문구분'])  # 출력: -매도, +매수
        order_gubun = order_gubun.strip().lstrip('+').lstrip('-')

        chegual_time_str = self.dynamicCall("GetChejanData(int)",
                                            REAL_TYPE.REALTYPE['주문체결']['주문/체결시간'])  # 출력: '151028'

        chegual_price = self.dynamicCall("GetChejanData(int)",
                                         REAL_TYPE.REALTYPE['주문체결']['체결가'])  # 출력: 2110 default : ''
        ## 처음 지정가 주문을 넣었을때 아직 체결된 수량이 없으므로 반값을 리
        if chegual_price == '':
            chegual_price = 0
        else:
            chegual_price = int(chegual_price)

        chegual_quantity = self.dynamicCall("GetChejanData(int)",
                                            REAL_TYPE.REALTYPE['주문체결']['체결량'])  # 출력: 5 default : ''
        if chegual_quantity == '':
            chegual_quantity = 0
        else:
            chegual_quantity = int(chegual_quantity)

        current_price = self.dynamicCall("GetChejanData(int)", REAL_TYPE.REALTYPE['주문체결']['현재가'])  # 출력: -6000
        current_price = abs(int(current_price))

        first_sell_price = self.dynamicCall("GetChejanData(int)",
                                            REAL_TYPE.REALTYPE['주문체결']['(최우선)매도호가'])  # 출력: -6010
        first_sell_price = abs(int(first_sell_price))

        first_buy_price = self.dynamicCall("GetChejanData(int)",
                                           REAL_TYPE.REALTYPE['주문체결']['(최우선)매수호가'])  # 출력: -6000
        first_buy_price = abs(int(first_buy_price))

        return StockOpenOrderBase(
            name=stock_name,
            code=sCode,
            status=order_status,
            order_quantity=order_quantity,
            unfill_quantity=unfill_quantity,
            price=order_price,
            gubun=order_gubun,
            number=order_number,
            origin_number=origin_order_number
        )