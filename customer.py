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

        returns dict with:
            id_string: [[left hash, left r1], [right hash, right r1]]
            reveal_string: [[left generated nums], [right generated nums]]
        '''
        IL = {}
        IR = {}

        r, s = self.secret_splitting()
        l_hash, r1, r2 = self.bit_commitment(id_int=r)
        r_hash, s1, s2 = self.bit_commitment(id_int=s)
        id_string = [[l_hash, r1], [r_hash, s1]]
        reveal_array = [[r, r1, r2], [s, s1, s2]]

        return {'id_string':id_string, 'reveal_array':reveal_array}


    def random_num_generator(self):
        '''Generates a random number'''
        # Parameters for random number generation
        rand_low_num = 100
        rand_high_num = 10000
        return random.randint(rand_low_num, rand_high_num)


    def reveal(self, moneyorders):
        '''Reveals identity pieces for requested moneyorders
        Takes in a list of money order keys (mo1, mo2, etc)

        Returns self.moneyorders[mo*][r/s,r1,r2]
        '''
        revealed_nums = {}
        for mo in moneyorders:
            orig_mo = self.moneyorders[mo]
            revealed_nums[mo] = {}
            for key in orig_mo.keys():
                if key.startswith('I'):
                    revealed_nums[mo][key] = orig_mo[key]['reveal_array']

        return revealed_nums
