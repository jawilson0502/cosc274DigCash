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
            self.moneyorders[mo_name] = self.create_moneyorder(mo_name)

    def create_moneyorder(self, name):
        '''Creates an dict containing necessary money order fields'''
        mo = {}
        mo['name'] = name
        mo['amount'] = self.amount
        mo['uniqueness'] = self.random_num_generator()
        mo['k'] = self.random_num_generator()
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
        self.blind_moneyorders = {}
        # Store keys['n'] as local variable due to wide use
        n = self.keys['n']

        # Iterate through all money orders to blind them
        for mo in self.moneyorders.keys():
            # Create a container for blinded money order being built
            blind_mo = {}
            # Pull original money order to work from
            orig_mo = self.moneyorders[mo]
            #Create blinding factor
            blind_factor = orig_mo['k'] ** self.keys['e'] % n

            # Start blinding process
            blind_mo['name'] = orig_mo['name']
            blind_mo['amount'] = (orig_mo['amount'] * blind_factor % n)
            blind_mo['uniqueness'] = (orig_mo['uniqueness'] * blind_factor % n)

            # Iterate through keys in money order and find identity string keys
            for key in orig_mo.keys():
                if not key.startswith('I'):
                    continue
                # Blind id_string section in I*
                # id_string is 2 element list containing a list of 2 elements
                blind_mo[key] = []
                for i in orig_mo[key]['id_string']:
                    blind_hash = (i[0] * blind_factor % n)
                    blind_random = (i[1] * blind_factor % n)
                    blind_mo[key].append([blind_hash, blind_random])

            self.blind_moneyorders[mo] = blind_mo


    def unblind(self, moneyorders):
        '''Unblinding process for money order

        Expects a list of money order names to be supplied.

        Sets unblinded_moneyorders variable.
        '''
        # Self variable to hold unblinded money orders
        self.unblinded_moneyorders = {}
        # Store keys['n'] as local variable due to wide use
        n = self.keys['n']

        # Iterate through all given money orders keys to unblind them
        for mo in moneyorders:
            # Create local variables for original and unblinded money orders
            orig_mo = self.moneyorders[mo]
            blind_mo = self.blind_moneyorders[mo]

            # Create the unblinding factor
            inv_k = int(gmpy.invert(orig_mo['k'], n))
            unblind_factor = (inv_k ** self.keys['e']) % n

            # Empty container for each unblinding money order
            unblind_mo = {}
            #Start the unblinding processes
            unblind_mo['name'] = orig_mo['name']
            unblind_mo['amount'] = (blind_mo['amount'] * unblind_factor % n)
            unblind_mo['uniqueness'] = (blind_mo['uniqueness'] * unblind_factor
                                        % n)
            # Iterate through keys in money order and find identity string keys
            for key in blind_mo.keys():
                if not key.startswith('I'):
                    continue
                unblind_mo[key] = {'id_string': []}
                for i in blind_mo[key]:
                    unblind_hash = (i[0] * unblind_factor % n)
                    unblind_random = (i[1] * unblind_factor % n)
                    unblind_mo[key]['id_string'].append([unblind_hash,
                                                         unblind_random])

            self.unblinded_moneyorders[mo] = unblind_mo


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
        return random.randint(rand_low_num, rand_high_num) % self.keys['n']


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
