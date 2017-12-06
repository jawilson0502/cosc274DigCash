''' Creates Customer class for digital cash transactions'''
import hashlib
import random

import gmpy

class Customer(object):
    def __init__(self, amount, identity, keys):
        self.amount = amount
        self.identity = identity
        self.keys = keys
        self.moneyorders = {}

        # Create 3 different money orders.
        for i in range(1, 4):
            mo_name = "mo" + str(i)
            self.moneyorders[mo_name] = self.create_moneyorder()

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
        # Self variable to hold blinded money orders
        self.blind_moneyorders = []

        for mo in self.moneyorders:
            blind_mo = {}
            blind_mo['k'] = mo['k']
            blind_mo['amount'] = (mo['amount'] * mo['blinding_factor']
                                  % self.keys['n'])
            blind_mo['uniqueness'] = (mo['uniqueness'] * mo['blinding_factor']
                                      % self.keys['n'])
            identity_strings = ['I1', 'I2', 'I3']
            for part in identity_strings:
                blind_mo[part] = []
                for i in mo[part]['id_string']:
                    blind_hash = (i[0] * mo['blinding_factor']
                                  % self.keys['n'])
                    blind_random = (i[1] * mo['blinding_factor']
                                    % self.keys['n'])
                    blind_mo[part].append([blind_hash, blind_random])

            self.blind_moneyorders.append(blind_mo)


    def unblind(self, moneyorders):
        '''Unblinding process for money order

        Expects a list of money orders to be supplied.

        Sets unblinded_moneyorders variable.
        '''
        self.unblinded_moneyorders = []
        for mo in moneyorders:
            inv_k = int(gmpy.invert(mo['k'], self.keys['n'])) % self.keys['n']
            unblinding_factor = (inv_k ** self.keys['e']) % self.keys['n']
            unblind_mo = {}
            unblind_mo['amount'] = (mo['amount'] * unblinding_factor
                                    % self.keys['n'])
            unblind_mo['uniqueness'] = (mo['uniqueness'] * unblinding_factor
                                        % self.keys['n'])
            identity_strings = ['I1', 'I2', 'I3']
            for part in identity_strings:
                unblind_mo[part] = []
                for i in mo[part]:
                    unblind_hash = (i[0] * unblinding_factor
                                  % self.keys['n'])
                    unblind_random = (i[1] * unblinding_factor
                                    % self.keys['n'])
                    unblind_mo[part].append([unblind_hash, unblind_random])

            self.unblinded_moneyorders.append(unblind_mo)


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
        int_value = int(hash_value, 16) % self.keys['n']

        return [int_value, r1, r2]


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
        id_string = [[IL['hash'], IL['r1']], [IR['hash'],IR['r1']]]

        return {'IL':IL, 'IR':IR, 'id_string':id_string}


    def random_num_generator(self):
        '''Generates a random number'''
        # Parameters for random number generation
        rand_low_num = 100
        rand_high_num = 10000
        return random.randint(rand_low_num, rand_high_num)
