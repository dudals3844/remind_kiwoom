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
from kiwoom.slot.real_slot import RealSlot
from kiwoom.slot.balance_open_order_slot import BalanceOpenOrderSlot

s
class Trading(QAxWidget):
    def __init__(self):
        super().__init__()
        print("Kiwoom start")
        self.get_ocx_instance()
        LoginSlot.connect(self, self.login_slot)
        TrSlot.connect(self, self.trdata_slot)
        RealSlot.connect(self, self.realdata_slot)
        BalanceOpenOrderSlot.connect(self, self.balance_openorder_slot)

        Login.request(self)
        Account.receive_number(self)
        Account.Deposit.request(self)
        Account.HoldStock.request(self)
        Account.OpenPositionStock.request(self)

    def get_ocx_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def login_slot(self, err_code):
        print(errors(err_code)[1])
        TR_EVENTLOOP.exit()

    def trdata_slot(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
        if sRQName == '예수금상세현황요청':
            Account.Deposit.receive(self, sTrCode, sRQName)
        elif sRQName == '계좌평가잔고내역요청':
            Account.HoldStock.receive(self, sRQName, sTrCode, sPrevNext)
        elif sRQName == '실시간미체결요청':
            Account.OpenPositionStock.receive(self, sTrCode, sRQName)

    def realdata_slot(self, sCode, sRealType, sRealData):
        if sRealType == '장시작시간':
            pass
        elif sRealType == "주식체결":
            pass

    def balance_openorder_slot(self, sGubun, nItemCnt, sFidList):
        # 주문체결
        if int(sGubun) == 0:
            pass
        # 잔고
        elif int(sGubun) == 1:
            pass
