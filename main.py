from kiwoom.kiwoom import Kiwoom
import sys
from PyQt5.QtWidgets import *

from kiwoom.trading import Trading


class Main:
    def __init__(self):
        print('Main start')

        self.app = QApplication(sys.argv)
        self.kiwoom = Trading()
        self.app.exec_()

if __name__ == '__main__':
    Main()