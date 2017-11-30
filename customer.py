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
        '''Generates a specified number of unique random numbers

        qty is the quantity of random numbers requested

        Returns unique array of random numbers
        '''
        rand_low_num = 100
        rand_high_num = 1000

        random_numbers = []

        while len(random_numbers) < qty:
            rand_int = random.randomint(rand_low_num, rand_high_num)
            if rand_int not in random_numbers:
                random_numbers.append(rand_int)

        return random_numbers
