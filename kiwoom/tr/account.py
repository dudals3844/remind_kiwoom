from property.global_variable import ACCOUNT_DATA, TR_EVENTLOOP, HOLD_STOCK_LIST, OPEN_ORDER_STOCK_LIST
from property.open_order_stock_dataclass import StockOpenOrderData
from property.screen_number import ScreenNumber
from property.stock_dataclass import StockData


class Account:
    def receive_number(self):
        account_list = self.dynamicCall('GetLoginInfo(QString)', 'ACCNO')
        account_num = account_list.split(';')[0]
        print(f'계좌번호: {account_num}')
        ACCOUNT_DATA.number = account_num

    class Deposit:
        def request(self, sPrevNext='0'):
            self.dynamicCall("SetInputValue(QString, QString)", "계좌번호", ACCOUNT_DATA.number)
            self.dynamicCall("SetInputValue(QString, QString)", "비밀번호", "0000")
            self.dynamicCall("SetInputValue(QString, QString)", "비밀번호입력매체구분", "00")
            self.dynamicCall("SetInputValue(QString, QString)", "조회구분", "1")
            self.dynamicCall("CommRqData(QString, QString, int, QString)", "예수금상세현황요청", "opw00001", sPrevNext,
                             ScreenNumber.MY_INFO.value)

        def receive(self, sTrCode, sRQName):
            deposit = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, '예수금')
            ACCOUNT_DATA.deposit = int(deposit)
            print(f"{deposit}")

    class HoldStock:
        def request(self, sPrevNext="0"):
            self.dynamicCall("SetInputValue(QString, QString)", "계좌번호", ACCOUNT_DATA.number)
            self.dynamicCall("SetInputValue(QString, QString)", "비밀번호", "0000")
            self.dynamicCall("SetInputValue(QString, QString)", "비밀번호입력매체구분", "00")
            self.dynamicCall("SetInputValue(QString, QString)", "조회구분", "1")
            self.dynamicCall("CommRqData(QString, QString, int, QString)", "계좌평가잔고내역요청", "opw00018", sPrevNext,
                             ScreenNumber.MY_INFO.value)
            TR_EVENTLOOP.exec_()


        def receive(self, sRQName, sTrCode, sPrevNext) -> list:
            ACCOUNT_DATA.total_buy_money = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode,
                                                            sRQName, 0, "총매입금액")
            ACCOUNT_DATA.total_profit_loss_money = self.dynamicCall("GetCommData(QString, QString, int, QString)",
                                                                    sTrCode, sRQName,
                                                                    0, "총평가손익금액")
            ACCOUNT_DATA.total_profit_loss_rate = self.dynamicCall("GetCommData(QString, QString, int, QString)",
                                                                   sTrCode, sRQName,
                                                                   0, "총수익률(%)")
            rows = self.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRQName)
            for i in range(rows):
                code = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "종목번호")
                code = code.strip()[1:]

                name = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "종목명")
                hold_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                                 "보유수량")
                buy_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "매입가")
                profit = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                          "수익률(%)")

                total_hold_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName,
                                                    i, "매입금액")

                name = name.strip()
                hold_quantity = int(hold_quantity.strip())
                buy_price = int(buy_price.strip())
                profit = float(profit.strip())
                total_hold_price = int(total_hold_price.strip())

                HOLD_STOCK_LIST.append(StockData(code=code,
                                                 name=name,
                                                 hold_quantity=hold_quantity,
                                                 buy_price=buy_price,
                                                 total_hold_price=total_hold_price,
                                                 profit=profit))


            if sPrevNext == "2":
                Account.HoldStock.request(self, sPrevNext='2')
            else:
                TR_EVENTLOOP.exit()

    class OpenPositionStock:
        def request(self, sPrevNext="0"):
            self.dynamicCall("SetInputValue(QString, QString)", "계좌번호", ACCOUNT_DATA.number)
            self.dynamicCall("SetInputValue(QString, QString)", "체결구분", "1")
            self.dynamicCall("SetInputValue(QString, QString)", "매매구분", "0")
            self.dynamicCall("CommRqData(QString, QString, int, QString)", "실시간미체결요청", "opt10075", sPrevNext,
                             ScreenNumber.MY_INFO.value)
            TR_EVENTLOOP.exec_()

        def receive(self, sTrCode, sRQName):
            rows = self.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRQName)
            self.__get(rows, sTrCode, sRQName)
            TR_EVENTLOOP.exit()

        def __get(self, rows, sTrCode, sRQName):
            for i in range(rows):
                code = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "종목코드")

                name = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "종목명")
                order_number = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                                "주문번호")
                order_status = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                                "주문상태")  # 접수,확인,체결
                order_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                                  "주문수량")
                order_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                               "주문가격")
                order_gubun = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                               "주문구분")  # -매도, +매수, -매도정정, +매수정정
                unfill_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                                   "미체결수량")

                code = code.strip()
                name = name.strip()
                order_number = int(order_number.strip())
                order_status = order_status.strip()
                order_quantity = int(order_quantity.strip())
                order_price = int(order_price.strip())
                order_gubun = order_gubun.strip().lstrip('+').lstrip('-')
                unfill_quantity = int(unfill_quantity.strip())

                OPEN_ORDER_STOCK_LIST.append(StockOpenOrderData(
                    name=name,
                    code=code,
                    number=order_number,
                    status=order_status,
                    order_quantity=order_quantity,
                    price=order_price,
                    gubun=order_gubun,
                    unfill_quantity=unfill_quantity
                ))
