''' Creates Customer class for digital cash transactions'''
import hashlib
import itertools
import random

class Customer(object):
    def __init__(self, amount, identity, keys):
        self.amount = amount
        self.identity = identity
        self.keys = keys
        self.moneyorders = []

        # Create 3 different money orders.
        for _ in itertools.repeat(None, 3):
            self.moneyorders.append(self.create_moneyorder())

    def create_moneyorder(self):
        '''Creates an dict containing necessary money order fields'''
        mo = {}
        mo['amount'] = self.amount
        mo['uniqueness'] = self.random_num_generator()
        mo['k'] = self.random_num_generator()
        mo['blinding_factor'] = (mo['k'] ** self.keys['e']) % self.keys['n']
        mo['I1'] = self.create_identity_string()
        mo['I2'] = self.create_identity_string()
        mo['I3'] = self.create_identity_string()

        return mo


    def print_moneyorder(self):
        '''Method to print money order to file'''
        pass


    def blind(self):
        '''Blinding process for money order

        Uses supplied secret to blind based on self.keys

        Returns blinded information
        '''
        pass


    def unblind(self):
        '''Unblinding process for money order'''
        pass


    def secret_splitting(self):
        '''Secret splitting process

        Uses self.identity to create r and s.

        Returns r and s
        '''
        r = self.random_num_generator()
        s = r ^ self.identity

        return r,s


    def bit_commitment(self, id_int):
        '''Bit commitment process

        Using supplied split secret id_int use sha256 to create bit commitment

        Return an array containing hash value and 2 randomly generated numbers
        '''
        # Get two random numbers
        r1 = self.random_num_generator()
        r2 = self.random_num_generator()

        # Calculate the hash of the id int and the random numbers
        # SHA256 library requires strings not integers, so ints are
        # concatentated together and then hashed
        int_string = str(id_int) + str(r1) + str(r2)
        byte_string = bytes(int_string, encoding='utf-8')
        hash_value = hashlib.sha256(byte_string).hexdigest()

        return [hash_value, r1, r2]


    def create_identity_string(self):
        '''Creates the necessary pieces of the identity string

        Returns IL and IR with dictionary keys:
            'r'|'s': Result of secret splitting
            'r1': First randomly generated number
            'r2': Second randomly generated number
            'hash': SHA256 hash of r/s and randomly generated numbers
        '''
        IL = {}
        IR = {}

        IL['r'], IR['s'] = self.secret_splitting()
        IL['hash'], IL['r1'], IL['r2'] = self.bit_commitment(id_int=IL['r'])
        IR['hash'], IR['r1'], IR['r2'] = self.bit_commitment(id_int=IR['s'])

        return {'IL':IL, 'IR':IR}


    def random_num_generator(self):
        '''Generates a random number'''
        # Parameters for random number generation
        rand_low_num = 100
        rand_high_num = 10000
        return random.randint(rand_low_num, rand_high_num)
