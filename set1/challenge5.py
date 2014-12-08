'''
Created on 3 Oct 2014

@author: simonm
'''

import array
from itertools import cycle

def xor_encrypt(string, key):
    byte_arr = array.array('B', string)
    key_arr  = array.array('B', key)
    result_arr = [b ^ k for b, k in zip(byte_arr, cycle(key_arr))]
    return "".join("{:02x}".format(b) for b in result_arr)

if __name__ == '__main__':
    
    string = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    key = "ICE"
    expected = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
    
    print(xor_encrypt(string, key) == expected)
   
