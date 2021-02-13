from property.global_variable import ACCOUNT_DATA

class Account:
    def get_info(self):
        account_list = self.dynamicCall('GetLoginInfo(QString)', 'ACCNO')
        account_num = account_list.split(';')[0]
        print(f'계좌번호: {account_num}')
        ACCOUNT_DATA.number = account_num