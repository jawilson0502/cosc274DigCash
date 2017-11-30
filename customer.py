''' Creates Customer class for digital cash transactions'''

class Customer(object):
    def __init__(self, amount, identity, keys):
        self.amount = amount
        self.identity = identity
        self.keys = keys

    def print_moneyorder(self):
        '''Method to print money order to file'''
        pass

    def blind(self):
        '''Blinding process for money order'''
        pass


    def unblind(self):
        '''Unblinding process for money order'''
        pass


    def secret_splitting(self):
        '''Secret splitting process'''
        pass

    def bit_commitment(self):
        '''Bit commitment process'''
        pass

    def random_num_generator(self, qty):
        '''Generates a specified number of unique random numbers'''
        pass
