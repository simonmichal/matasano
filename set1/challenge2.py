'''
Created on 2 Oct 2014

@author: simonm
'''

import array

def xor_bytes(hexstr1, hexstr2):
    # decode the input
    hex_data1 = hexstr1.decode('hex')
    hex_data2 = hexstr2.decode('hex')
    # and put it into a byte array
    byte_arr1 = array.array('B', hex_data1)
    byte_arr2 = array.array('B', hex_data2)
    # create a byte array of xors
    result_arr = [b1 ^ b2 for b1, b2 in zip(byte_arr1, byte_arr2)]
    # encode the result array to hex
    return "".join("{:02x}".format(b) for b in result_arr)

if __name__ == '__main__':
    
    hexstr1 = '1c0111001f010100061a024b53535009181c'
    hexstr2 = '686974207468652062756c6c277320657965'
    expected = '746865206b696420646f6e277420706c6179'
    
    print(xor_bytes(hexstr1, hexstr2) == expected)
    
