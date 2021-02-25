from property.enum.screen_number_enum import ScreenNumberEnum
from property.global_variable import ACCOUNT_DATA, REAL_TYPE
from property.enum.order_type_enum import OrderTypeEnum
from kiwoom.order.order_status import OrderStatus


class Mesu:
    class Market:
        def order(self, code, quantity) -> bool:
            order_status = self.dynamicCall("SendOrder(QString,QString,QString,int,QString,int,int,QString,QString)",
                                            ['신규매수', ScreenNumberEnum.ORDER.value, ACCOUNT_DATA.number,
                                             OrderTypeEnum.MESU.value, code,
                                             quantity,
                                             0, REAL_TYPE.SENDTYPE['거래구분']['시장가'], ''])
            return OrderStatus.is_success(order_status)

    class Limit:
        def order(self, code, quantity, price) -> bool:
            order_status = self.dynamicCall("SendOrder(QString,QString,QString,int,QString,int,int,QString,QString)",
                                            ['신규매수', ScreenNumberEnum.ORDER.value, ACCOUNT_DATA.number,
                                             OrderTypeEnum.MESU.value, code,
                                             quantity,
                                             price, REAL_TYPE.SENDTYPE['거래구분']['지정가'], ''])
            return OrderStatus.is_success(order_status)

        def cancel_order(self, code, order_number) -> bool:
            order_status = self.dynamicCall("SendOrder(QString,QString,QString,int,QString,int,int,QString,QString)",
                                            ['매수취소', ScreenNumberEnum.ORDER.value, ACCOUNT_DATA.number, OrderTypeEnum.CANCEL_MESU.value, code, 0,
                                             0, REAL_TYPE.SENDTYPE['거래구분']['지정가'], order_number])
            return OrderStatus.is_success(order_status)
