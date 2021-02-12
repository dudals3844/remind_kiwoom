from PyQt5.QAxContainer import *
from PyQt5.QtCore import QEventLoop, QTimer
from PyQt5.QtTest import QTest
from config.errorCode import *
from config.kiwoomType import RealType
from kiwoom.tr.login import Login

class Trading(QAxWidget):
    def __init__(self):
        super().__init__()
        print("Kiwoom start")
        self.get_ocx_instance()
        Login.request(self)

    def get_ocx_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")
