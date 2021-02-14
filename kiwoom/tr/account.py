from property.global_variable import ACCOUNT_DATA
from property.screen_number import ScreenNumber


class Account:
    def receive_info(self):
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
