'''
Created on 24 Sep 2014

@author: simonm
'''

import array

class Base64:
    
    def __init__(self, hexstr) :
        # the hex string + taking care of padding
        padding = len(hexstr) % 6
        self.hexstr = hexstr if padding == 0 else '0' * (6 - padding) + hexstr
        self.base64str = ''
        # these are the possible transitions
        self.transition = {(0, 6) : (6, 2), (6, 2) : (0, 4), (0, 4) : (4, 4), (4, 4) : (0, 2), (0, 2) : (2, 6), (2, 6) : (0, 6)}
        # these are the possible values for a 64-base
        self.values = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
        # the number of bits that have been set
        self.bitsum = 0

    def move_bits(self, byte, count, start):
        ret = 0
        # start shifting the bits from the end to the beginning
        # (there are 8 bits per byte ;)
        for i in xrange(7 - start, 7 - start - count, -1):
            ret = ret << 1 # make place for next bit
            ret |= 0 if (byte & (1 << i)) == 0 else 1 # assign a value to the empty bit
        return ret
        
    def next_bits(self, byte, start, index, count):
        # make place for the new bits
        index = index << count
        # assign bits
        index |= self.move_bits(byte, count, start)
        # update the number of bits that have been assigned
        self.bitsum += count
        # 6 is our number (2^6=64)
        if self.bitsum == 6:
            self.base64str += self.values[index] # get the mapping 
            index = self.bitsum = 0 # reset index and bitsum
        # check where is the start of the next number and how many bits should we read
        start, count = self.transition[start, count]; 
        # return the new parameters
        return start, index, count
        
    def value(self):
        # decode the input
        hex_data = self.hexstr.decode('hex')
        # and put it into a byte array
        arr = array.array('B', hex_data)
        # start with the first bit on the left
        start = index = 0
        # get first 6 bits looking from left to right
        count = 6
        # process each byte 
        for byte in arr :
            # there are two calls per byte because 6 < 8 ;)
            start, index, count = self.next_bits(byte, start, index, count)
            start, index, count = self.next_bits(byte, start, index, count)
        return self.base64str

if __name__ == '__main__':
    
    expected = 'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'
    hexstr = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
    
    base64 = Base64(hexstr)
    print(base64.value() == expected)