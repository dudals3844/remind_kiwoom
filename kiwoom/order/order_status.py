

class OrderStatus:

    @staticmethod
    def is_success(order_status):
        if order_status == 0:
            return True
        else:
            return False