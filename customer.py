''' Creates Customer class for digital cash transactions'''
import random

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
        # Parameters for random number generation
        rand_low_num = 100
        rand_high_num = 1000

        # Empty array to place random numbers in to be returned
        random_numbers = []

        # Create the random numbers, and ensure each is unique within the array
        while len(random_numbers) < qty:
            rand_int = random.randomint(rand_low_num, rand_high_num)
            if rand_int not in random_numbers:
                random_numbers.append(rand_int)

        return random_numbers
