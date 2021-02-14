from PyQt5.QAxContainer import *
from PyQt5.QtCore import QEventLoop, QTimer
from PyQt5.QtTest import QTest
from config.errorCode import *
from config.kiwoomType import RealType
from kiwoom.tr.account import Account
from property.global_variable import TR_EVENTLOOP, ACCOUNT_DATA
from kiwoom.tr.login import Login
from kiwoom.slot.login_slot import LoginSlot
from kiwoom.slot.tr_slot import TrSlot


class Trading(QAxWidget):
    def __init__(self):
        super().__init__()
        print("Kiwoom start")
        self.get_ocx_instance()
        LoginSlot.connect(self, self.login_slot)
        TrSlot.connect(self, self.trdata_slot)

        Login.request(self)
        Account.receive_info(self)
        Account.Deposit.request(self)


    def get_ocx_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def login_slot(self, err_code):
        print(errors(err_code)[1])
        TR_EVENTLOOP.exit()

    def trdata_slot(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
        if sRQName == '예수금상세현황요청':
            Account.Deposit.receive(self, sTrCode, sRQName)
