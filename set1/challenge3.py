'''
Created on 2 Oct 2014

@author: simonm
'''

import array
import re

def decode(hexstr, char):
    # decode the input
    hex_data = hexstr.decode('hex')
    # and put it into a byte array
    byte_arr = array.array('B', hex_data)
    # decoded array
    result_arr = [b ^ char for b in byte_arr]
    # convert bytes to chars and append to string
    return "".join("{:c}".format(b) for b in result_arr)

def is_sentence(string):
    return re.match("^[\w '-?!.,:;()&]+$", string)

def print_decoded(hexstr):
    # loop over all characters
    for i in xrange(0, 256):
        # and try to decode using every single one
        string = decode(hexstr, i)
        # if the result contains only spaces, alphanumeric characters 
        # and punctuation characters print it
        if is_sentence(string): 
            print(string)

if __name__ == '__main__':
    hex_encoded = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    print_decoded(hex_encoded)
