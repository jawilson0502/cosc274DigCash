''' Creates Customer class for digital cash transactions'''
import hashlib
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
        '''Secret splitting process

        Uses self.identity to create r and s.

        Returns r and s
        '''
        r = self.random_num_generator(qty=1)
        s = r ^ self.identity

        return r,s


    def bit_commitment(self, id_int):
        '''Bit commitment process

        Using supplied split secret id_int use sha256 to create bit commitment

        Return an array containing hash value and 2 randomly generated numbers
        '''
        # Get two random numbers
        r1, r2 = self.random_num_generator(qty=2)

        # Calculate the hash of the id int and the random numbers
        # SHA256 library requires strings not integers, so ints are converted
        # to strings during hashing
        hash_value = hashlib.sha256()
        hash_value = hash_value.update(id_int)
        hash_value = hash_value.update(r1)
        hash_value = hash_value.update(r2)

        return [hash_value, r1, r2]


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
