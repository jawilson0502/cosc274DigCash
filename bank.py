'''Creates the bank class'''
import hashlib
import random

class Bank(object):
    def __init__(self, keys):
        print("Intializing Bank")
        self.keys = keys

    def calc_hash(self, int_array):
        '''Using supplied int_array, calculate hash'''
        int_string = str(int_array[0]) + str(int_array[1]) + str(int_array[2])
        byte_string = bytes(int_string, encoding='utf-8')
        hash_value = hashlib.sha256(byte_string).hexdigest()
        int_value = int(hash_value, 16) % self.keys['n']

        return int_value

    def calculate_verify(self):
        '''Verfies that revealed information matches blinded money order
        and all amounts are the same
        '''
        amounts = []
        for mo in self.to_unblind_moneyorders:
            reveal_info = self.reveal_info[mo]
            unblind_mo = self.unblind_moneyorders[mo]

            amounts.append(unblind_mo['amount'])

            for key in reveal_info.keys():
                id_string = unblind_mo[key]['id_string']

                left = reveal_info[key][0]
                right = reveal_info[key][1]

                calculated_left = [self.calc_hash(left), left[1]]
                calculated_right = [self.calc_hash(right), right[1]]
                calculated_id_string = [calculated_left, calculated_right]

                if not calculated_id_string == id_string:
                    print("MO: %s, Key: %s" % (mo, key))
                    print("calc: %s, given: %s" % (str(calculated_id_string),
                                                   str(id_string)))
                    return False
        amounts = set(amounts)
        if len(amounts) > 1:
            print("Amounts didn't match")
            return False
        return True


    def receive_blindmoneyorders(self, moneyorders):
        '''Receive blinded money orders from customer
        Sets self variable storing blinded money orders
        '''
        print("Bank Recieved Blind Money Orders")
        self.blind_moneyorders = moneyorders


    def receive_revealinfo(self, reveal_info):
        '''Receive reveal information for unblinded money orders
        Sets self variable storing real_info'''
        print("Bank Recieved Money Order Information")
        self.reveal_info = reveal_info


    def receive_unblindedmoneyorders(self, moneyorders):
        '''Receive unblinded money orders from customer
        Sets self variable storing unblinded money orders'''
        print("Bank Recieved Unblinded Money Orders")
        self.unblind_moneyorders = moneyorders

    def sign_moneyorder(self):
        '''Signs money order given'''
        if not self.calculate_verify():
            print('Cannot verify unblinded money orders')

        # If it can verify the unblinded money orders
        bank_signature = []
        d = self.keys['d']
        n = self.keys['n']
        blinded_mo = self.to_sign_moneyorder

        bank_signature.append(blinded_mo['amount'] ** d % n)
        bank_signature.append(blinded_mo['uniqueness'] ** d % n)
        id_keys = ['I1', 'I2', 'I3']
        for key in id_keys:
            for i in blinded_mo[key]['id_string']:
                bank_signature.append(i[0] ** d %n)
                bank_signature.append(i[1] ** d % n)
        print("Verified: Bank Signing")

        self.bank_signature = bank_signature

    def unblind_request(self):
        '''Creates list of money orders to be unblinded'''
        print("Bank Requested Unblinding")
        # Parameters for random number generation based on
        # length of blinded money orders received
        rand_low_num = 0
        rand_high_num = len(self.blind_moneyorders.keys()) - 1

        # Pick random index number to sign
        to_sign_mo_index = random.randint(rand_low_num, rand_high_num)

        # Create a list of all possible keys and select randomly chosen index
        key_list = list(self.blind_moneyorders.keys())
        to_sign_mo_key = key_list[to_sign_mo_index]

        # Set self variable to the blinded money order to sign
        self.to_sign_moneyorder_key = to_sign_mo_key
        self.to_sign_moneyorder = self.blind_moneyorders[to_sign_mo_key]

        # Create a self variable for all the money orders to unblind
        to_unblind_mo = list(self.blind_moneyorders.keys())
        to_unblind_mo.pop(to_unblind_mo.index(to_sign_mo_key))
        self.to_unblind_moneyorders = to_unblind_mo


    def verify_unblinded(self, moneyorder):
        '''Verifies all unblinded money orders have the same amount'''
        pass
