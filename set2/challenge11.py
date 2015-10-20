'''
Created on 20 Oct 2015

@author: simonm
'''

import random
import string
import array

from challenge10 import aes128

def random_byte():
    return chr(random.randrange(0, 256))

def random_bytes():
    count = random.randrange(5, 11)
    return ''.join(random_byte() for x in range(count))

def random_key():
    return ''.join(random.choice(string.ascii_letters) for x in range(16))
#     return ''.join(chr(random.randrange(33, 122)) for x in range(16))

def encrypt(txt):
    txt = random_bytes() + txt + random_bytes()
    key = random_key()
    e = aes128() 
    if random.randrange(0, 2) > 0:
        # ecb
        print("ecb")
        return e.encrypt_ecb(txt, key)
    else:
        # cbc
        print("cbc")
        iv = ''.join(random_byte() for x in range(16))
        return e.encrypt_cbc(txt, key, iv)

def detect_mode():
    plain = ''.join('a' for x in range(0, 16 * 3))
    txt = encrypt(plain)
    # in principle if we brake the output into rows of size 16 (key size) 
    # the second row and the third row should be the same (ECB is stateleless)
    ecb =  txt[1 * 16 : 2 * 16] == txt[2 * 16 : 3 * 16]
    print("ECB was used: ", ecb)
    

if __name__ == '__main__':
    detect_mode()