from PyQt5.QAxContainer import *
from PyQt5.QtCore import QEventLoop, QTimer
from PyQt5.QtTest import QTest

from config.errorCode import *
from config.kiwoomType import RealType


class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        print('Kiwoom start')
        self.get_ocx_instance()
        self.real_type = RealType()

        self.login_event_loop = QEventLoop()
        # 왜 Event loop를 안에다가 넣어야 될까
        self.detail_account_info_event_loop = QEventLoop()
        self.calculator_event_loop = QEventLoop()

        #### 계좌 관련 변수
        self.account_stock_dict  = {}
        self.not_account_stock_dict = {}
        self.calcul_data = []

        self.account_num = None
        self.deposit = 0
        self.use_money = 0
        self.use_money_percent = 0.5
        self.output_deposit = 0
        self.total_profit_loss_money = 0
        self.total_profit_loss_rate = 0

        self.screen_my_info = "2000"
        self.screen_calculation_stock = '4000'
        self.screen_start_stop_real = '1000'
        self.screen_real_stock_data = '1500'

        self.event_slots()
        self.real_event_slot()

        self.signal_login_commConnect()
        self.get_account_info()
        self.detail_account_info()
        self.detail_account_mystock()
        # QTimer.singleShot(5000, self.not_concluded_account)
        self.calculator_fnc()
        # 실시간 장시간 등
        self.dynamicCall("SetRealReg록(QString, QString, QString, QString)", self.screen_start_stop_real, '',
                         self.realType.REALTYPE['장시작시간']['장운영구분'], "0")

        fids = self.real_type.REALTYPE['주식체결']['체결시간']
        self.dynanicCall("SetRealReg(QString, QString, QString, QString)", self.screen_real_stock_data, '005930', fids, "1")

    def get_ocx_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def event_slots(self):
        self.OnEventConnect.connect(self.login_slot)
        self.OnReceiveTrData.connect(self.trdata_slot)

    def real_event_slot(self):
        self.OnReceiveRealData.connect(self.realdata_slot)

    def signal_login_commConnect(self):
        self.dynamicCall('CommConnect')
        self.login_event_loop.exec_()

    def login_slot(self, err_code):
        print(errors(err_code)[1])
        self.login_event_loop.exit()


    def realdata_slot(self, sCode, sRealType, sRealData):
        if sRealType == '장시작시간':
            fid = self.real_type.REALTYPE[sRealType]['장운영구분']
            value = self.dynamicCall("GetCommRealData(QString, int)", sCode, fid)
            if value == '0':
                print('장 시작전')
            elif value == '3':
                print('장 시작')
            elif value == '2':
                print('장 종료: 동시호가로 넘어감')
            elif value == '4':
                print('3시 30분 장 종')

        elif sRealType == "주식체결":
            time = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                 self.realType.REALTYPE[sRealType]['체결시간'])  # 출력 HHMMSS
            now_price = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                 self.realType.REALTYPE[sRealType]['현재가'])  # 출력 : +(-)2520
            now_price = abs(int(b))

            yesterday_diff = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                 self.realType.REALTYPE[sRealType]['전일대비'])  # 출력 : +(-)2520
            yesterday_diff = abs(int(yesterday_diff))

            yesterday_diff_percent = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                                      self.realType.REALTYPE[sRealType]['등락율'])  # 출력 : +(-)12.98
            yesterday_diff_percent = float(yesterday_diff_percent)

            medo_1_hoga = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                           self.realType.REALTYPE[sRealType]['(최우선)매도호가'])  # 출력 : +(-)2520
            medo_1_hoga = abs(int(medo_1_hoga))

            mesu_1_hoga = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                           self.realType.REALTYPE[sRealType]['(최우선)매수호가'])  # 출력 : +(-)2515
            mesu_1_hoga = abs(int(mesu_1_hoga))

            volume = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                      self.realType.REALTYPE[sRealType]['거래량'])  # 출력 : +240124 매수일때, -2034 매도일 때
            volume = abs(int(volume))

            volume_sum = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                          self.realType.REALTYPE[sRealType]['누적거래량'])  # 출력 : 240124
            volume_sum = abs(int(volume_sum))

            high_price = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                          self.realType.REALTYPE[sRealType]['고가'])  # 출력 : +(-)2530
            high_price = abs(int(high_price))

            start_price = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                           self.realType.REALTYPE[sRealType]['시가'])  # 출력 : +(-)2530
            start_price = abs(int(start_price))

            low_price = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                         self.realType.REALTYPE[sRealType]['저가'])  # 출력 : +(-)2530
            low_price = abs(int(low_price))



    def trdata_slot(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
        if sRQName == '예수금상세현황요청':
            deposit = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, '예수금')
            self.deposit = int(deposit)

            use_money = float(self.deposit) * self.use_money_percent
            self.use_money = int(use_money) / 4
            output_deposit = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, '출금가능금액')
            self.output_deposit = int(output_deposit)
            print(f'예수금: {self.output_deposit}')

        elif sRQName == '계좌평가잔고내역요청':
            total_buy_money = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0,
                                               "총매입금액")
            self.total_buy_money = int(total_buy_money)
            total_profit_loss_money = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName,
                                                       0, "총평가손익금액")
            self.total_profit_loss_money = int(total_profit_loss_money)
            total_profit_loss_rate = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName,
                                                      0, "총수익률(%)")
            self.total_profit_loss_rate = float(total_profit_loss_rate)
            print(f'계좌평가잔고내역요청: {self.total_buy_money}, {self.total_profit_loss_money}, {self.total_profit_loss_rate}')

            rows = self.dynamicCall("GetRepeatCnt(QString, QString)",sTrCode, sRQName)
            for i in range(rows):
                code = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "종목번호")
                code = code.strip()[1:]

                code_nm = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "종목명")
                stock_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                                  "보유수량")
                buy_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "매입가")
                learn_rate = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                              "수익률(%)")
                current_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                                 "현재가")
                total_chegual_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName,
                                                       i, "매입금액")
                possible_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                                     "매매가능수량")

                print("종목번호: %s - 종목명: %s - 보유수량: %s - 매입가:%s - 수익률: %s - 현재가: %s" % (
                code, code_nm, stock_quantity, buy_price, learn_rate, current_price))

                if code in self.account_stock_dict:
                    pass
                else:
                    self.account_stock_dict[code] = {}

                code_nm = code_nm.strip()
                stock_quantity = int(stock_quantity.strip())
                buy_price = int(buy_price.strip())
                learn_rate = float(learn_rate.strip())
                current_price = int(current_price.strip())
                total_chegual_price = int(total_chegual_price.strip())
                possible_quantity = int(possible_quantity.strip())

                self.account_stock_dict[code].update({"종목명": code_nm})
                self.account_stock_dict[code].update({"보유수량": stock_quantity})
                self.account_stock_dict[code].update({"매입가": buy_price})
                self.account_stock_dict[code].update({"수익률(%)": learn_rate})
                self.account_stock_dict[code].update({"현재가": current_price})
                self.account_stock_dict[code].update({"매입금액": total_chegual_price})
                self.account_stock_dict[code].update({"매매가능수량": possible_quantity})

            print("sPreNext : %s" % sPrevNext)
            print("계좌에 가지고 있는 종목은 %s " % rows)

            if sPrevNext == "2":
                self.detail_account_mystock(sPrevNext="2")
            else:
                self.detail_account_info_event_loop.exit()

        elif sRQName == "실시간미체결요청":
            rows = self.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRQName)

            for i in range(rows):
                code = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "종목코드")

                code_nm = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "종목명")
                order_no = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "주문번호")
                order_status = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                                "주문상태")  # 접수,확인,체결
                order_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                                  "주문수량")
                order_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                               "주문가격")
                order_gubun = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                               "주문구분")  # -매도, +매수, -매도정정, +매수정정
                not_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                                "미체결수량")
                ok_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                               "체결량")

                code = code.strip()
                code_nm = code_nm.strip()
                order_no = int(order_no.strip())
                order_status = order_status.strip()
                order_quantity = int(order_quantity.strip())
                order_price = int(order_price.strip())
                order_gubun = order_gubun.strip().lstrip('+').lstrip('-')
                not_quantity = int(not_quantity.strip())
                ok_quantity = int(ok_quantity.strip())

                if order_no in self.not_account_stock_dict:
                    pass
                else:
                    self.not_account_stock_dict[order_no] = {}

                self.not_account_stock_dict[order_no].update({'종목코드': code})
                self.not_account_stock_dict[order_no].update({'종목명': code_nm})
                self.not_account_stock_dict[order_no].update({'주문번호': order_no})
                self.not_account_stock_dict[order_no].update({'주문상태': order_status})
                self.not_account_stock_dict[order_no].update({'주문수량': order_quantity})
                self.not_account_stock_dict[order_no].update({'주문가격': order_price})
                self.not_account_stock_dict[order_no].update({'주문구분': order_gubun})
                self.not_account_stock_dict[order_no].update({'미체결수량': not_quantity})
                self.not_account_stock_dict[order_no].update({'체결량': ok_quantity})

                print("미체결 종목 : %s " % self.not_account_stock_dict[order_no])

            self.detail_account_info_event_loop.exit()

        elif sRQName == "주식일봉차트조회":
            code = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "종목코드")
            code = code.strip()
            # data = self.dynamicCall("GetCommDataEx(QString, QString)", sTrCode, sRQName)

            cnt = self.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRQName)
            print("남은 일자 수 %s" % cnt)

            for i in range(cnt):
                data = []

                current_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                                 "현재가")  # 출력 : 000070
                value = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                         "거래량")  # 출력 : 000070
                trading_value = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                                 "거래대금")  # 출력 : 000070
                date = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                        "일자")  # 출력 : 000070
                start_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                               "시가")  # 출력 : 000070
                high_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                              "고가")  # 출력 : 000070
                low_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                             "저가")  # 출력 : 000070

                data.append("")
                data.append(current_price.strip())
                data.append(value.strip())
                data.append(trading_value.strip())
                data.append(date.strip())
                data.append(start_price.strip())
                data.append(high_price.strip())
                data.append(low_price.strip())
                data.append("")

                self.calcul_data.append(data.copy())
                print(f'price: {current_price}, date: {date}, value: {value}')

            if sPrevNext == "2":
                self.day_kiwoom_db(code=code, sPrevNext=sPrevNext)
            else:
                print(self.calcul_data)
                self.calculator_event_loop.exit()



    def get_account_info(self):
        account_list = self.dynamicCall('GetLoginInfo(QString)', 'ACCNO')
        account_num = account_list.split(';')[0]
        self.account_num = account_num
        print(f'계좌번호: {self.account_num}')

    def detail_account_info(self, sPrevNext = '0'):
        self.dynamicCall("SetInputValue(QString, QString)","계좌번호", self.account_num)
        self.dynamicCall("SetInputValue(QString, QString)","비밀번호", "0000")
        self.dynamicCall("SetInputValue(QString, QString)","비밀번호입력매체구분", "00")
        self.dynamicCall("SetInputValue(QString, QString)","조회구분", "1")
        self.dynamicCall("CommRqData(QString, QString, int, QString)","예수금상세현황요청", "opw00001", sPrevNext, self.screen_my_info)

    def detail_account_mystock(self, sPrevNext="0"):
        self.dynamicCall("SetInputValue(QString, QString)", "계좌번호", self.account_num)
        self.dynamicCall("SetInputValue(QString, QString)", "비밀번호", "0000")
        self.dynamicCall("SetInputValue(QString, QString)", "비밀번호입력매체구분", "00")
        self.dynamicCall("SetInputValue(QString, QString)", "조회구분", "1")
        self.dynamicCall("CommRqData(QString, QString, int, QString)", "계좌평가잔고내역요청", "opw00018", sPrevNext,
                         self.screen_my_info)
        self.detail_account_info_event_loop.exec_()

    def not_concluded_account(self, sPrevNext = "0"):
        print("미체결 종목 요청")
        self.dynamicCall("SetInputValue(QString, QString)", "계좌번호", self.account_num)
        self.dynamicCall("SetInputValue(QString, QString)", "체결구분", "1")
        self.dynamicCall("SetInputValue(QString, QString)", "매매구분", "0")
        self.dynamicCall("CommRqData(QString, QString, int, QString)", "실시간미체결요청", "opt10075", sPrevNext,
                         self.screen_my_info)

        self.detail_account_info_event_loop.exec_()

    def get_code_list_by_market(self, market_code):
        code_list = self.dynamicCall("GetCodeListByMarket(QString)", market_code)
        code_list = code_list.split(';')[:-1]
        return code_list

    def calculator_fnc(self):
        code_list = self.get_code_list_by_market("10")
        print("코스닥 갯수 %s " % len(code_list))

        for idx, code in enumerate(code_list):
            self.dynamicCall("DisconnectRealData(QString)", self.screen_calculation_stock)  # 스크린 연결 끊기

            print("%s / %s : KOSDAQ Stock Code : %s is updating... " % (idx + 1, len(code_list), code))
            self.day_kiwoom_db(code=code)

    def day_kiwoom_db(self, code=None, date=None, sPrevNext="0"):
        QTest.qWait(3600)  # 3.6초마다 딜레이를 준다.

        self.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)
        self.dynamicCall("SetInputValue(QString, QString)", "수정주가구분", "1")

        if date != None:
            self.dynamicCall("SetInputValue(QString, QString)", "기준일자", date)

        self.dynamicCall("CommRqData(QString, QString, int, QString)", "주식일봉차트조회", "opt10081", sPrevNext,
                         self.screen_calculation_stock)

        self.calculator_event_loop.exec_()

    def stop_screen_cancle(self, sScrNo = None):
        self.dynamicCall('DisconnectRealData(QString)', sScrNo)