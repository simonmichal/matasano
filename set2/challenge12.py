'''
Created on 28 Oct 2015

@author: simonm
'''

import base64
import string

from collections import Counter

from challenge10 import aes128



random_key = 'YHcTTdBjsPeoGOag'

def oracle(input, key=random_key):
    txt = 'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK'
    txt = base64.b64decode(txt)
    # your-string || unknown-string
    plain = input + txt
    enc = aes128()
    return enc.encrypt_ecb(plain, key)

def get_block_size():
    for i in range(1, 32):
        plain = b'A' * i * 2
        cipher = oracle(plain)
        if cipher[ : i] == cipher[i : 2 * i]:
            return i
    return None

def is_ecb():
    return get_block_size() != None

def get_dict(prefix):
    enc = aes128()
    dict= {}
    for char in range(256):
        plain = prefix + chr(char)
        k = enc.encrypt_ecb(plain, random_key)
        dict[k] = chr(char)
    return dict
    
def get_unknown_length():
    return len(oracle(''))
    
def decode():
    txt = ''
    blocksize = get_block_size()
    
    # init
    prefix = b'A' * (blocksize - 1)
    last_block = prefix;
    
    # decode each character one by one
    for i in range(get_unknown_length()):
        dict = get_dict(last_block)
        cipher = oracle(prefix)
        start = (i / blocksize)
        decoded_char = dict[cipher[start * blocksize : (start + 1) * blocksize]]
        txt += decoded_char
        # set up prefix for new iteration
        if not prefix: prefix = b'A' * (blocksize - 1)
        else: prefix = prefix[1 : ]
        # set up last block for new iteration
        last_block = last_block[1 : ] + decoded_char
        
    return txt          

if __name__ == '__main__':
    print(decode())