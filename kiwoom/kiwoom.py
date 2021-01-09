from PyQt5.QAxContainer import *

class Kiwoom(QAWidget):
    def __init__(self):
        super().__init__()
        print('Kiwoom start')
        self.get_ocx_instance()

    def get_ocx_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")


