'''Creates the bank class'''

class Bank(object):
    def __init__(self, keys):
        self.keys = keys

    def sign_moneyorder(self, money_order):
        '''Signs money order given'''
        pass

    
    def calculate_verify(self, money_order, reveal_info):
        '''Verfies that revealed information matches blinded money order'''
        pass


    def verify_unblinded(self, money_order):
        '''Verifies all unblinded money orders have the same amount'''
        pass
