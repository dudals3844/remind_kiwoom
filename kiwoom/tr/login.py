from property.constants import TR_EVENTLOOP

class Login:
    def request(self):
        self.dynamicCall("CommConnect()")
        TR_EVENTLOOP.exec_()