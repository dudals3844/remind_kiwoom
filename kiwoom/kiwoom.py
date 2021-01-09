from PyQt5.QAxContainer import *
from PyQt5.QtCore import QEventLoop
from config.errorCode import *

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        print('Kiwoom start')
        self.get_ocx_instance()

        self.login_event_loop = QEventLoop()

        #### 계좌 관련 변수
        self.account_num = None
        self.deposit = 0
        self.use_money = 0
        self.use_money_percent = 0.5
        self.output_deposit = 0

        self.screen_my_info = "2000"

        self.event_slots()
        self.signal_login_commConnect()
        self.get_account_info()
        self.detail_account_info()

    def get_ocx_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def event_slots(self):
        self.OnEventConnect.connect(self.login_slot)
        self.OnReceiveTrData.connect(self.trdata_slot)

    def signal_login_commConnect(self):
        self.dynamicCall('CommConnect')
        self.login_event_loop.exec_()

    def login_slot(self, err_code):
        print(errors(err_code)[1])
        self.login_event_loop.exit()

    def trdata_slot(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
        deposit = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, '예수금')
        self.deposit = int(deposit)

        use_money = float(self.deposit) * self.use_money_percent
        self.use_money = int(use_money) / 4
        output_deposit = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, '출금가능금액')
        self.output_deposit = int(output_deposit)
        print(f'예수금: {self.output_deposit}')
        self.stop_screen_cancle(self.screen_my_info)

    def get_account_info(self):
        account_list = self.dynamicCall('GetLoginInfo(QString)', 'ACCNO')
        account_num = account_list.split(';')[0]
        self.account_num = account_num
        print(f'계좌번호: {self.account_num}')

    def detail_account_info(self, sPreNext = '0'):
        self.dynamicCall("SetInputValue(QString, QString)","계좌번호", self.account_num)
        self.dynamicCall("SetInputValue(QString, QString)","비밀번호", "0000")
        self.dynamicCall("SetInputValue(QString, QString)","비밀번호입력매체구분", "00")
        self.dynamicCall("SetInputValue(QString, QString)","조회구분", "1")
        self.dynamicCall("CommRqData(QString, QString, int, QString)","예수금상세현황요청", "opw00001", sPreNext, self.screen_info)

    def stop_screen_cancle(self, sScrNo = None):
        self.dynamicCall('DisconnectRealData(QString)', sScrNo)