'''
Created on 18 Nov 2014

@author: simonm
'''

import array
import base64
import urllib2

def xor_bytes(byte_arr1, byte_arr2):
    # create a byte array of xors
    return array.array('B', [b1 ^ b2 for b1, b2 in zip(byte_arr1, byte_arr2)])

def xtime(x):
    return ((x<<1) ^ (((x>>7) & 1) * 0x1b))

def multiply(x, y):
    return 0xFF & (((y & 1) * x) ^ 
            ((y>>1 & 1) * xtime(x)) ^ 
            ((y>>2 & 1) * xtime(xtime(x))) ^ 
            ((y>>3 & 1) * xtime(xtime(xtime(x)))) ^ 
            ((y>>4 & 1) * xtime(xtime(xtime(xtime(x))))))  

class aes128:
    # the number of columns comprising a state in AES. This is a constant in AES. Value=4
    nb = 4
    # the number of 32 bit words in a key.
    nk = 4
    # key length in bytes (128 bit)
    keylen = 16
    # the number of rounds in AES Cipher.
    nr = 10
    # substitution-box
    sbox = [
    #   0     1     2     3     4     5     6     7     8     9     A     B     C     D     E     F
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16 
    ]
    #
    rsbox = [
        0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
        0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
        0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
        0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
        0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
        0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
        0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
        0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
        0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
        0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
        0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
        0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
        0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
        0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
        0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d 
    ]
    # the round constant word array, rcon[i], contains the values given by 
    # x to the power (i-1) being powers of x (x is denoted as {02}) in the field GF(2^8)
    # note that i starts at 1, not 0)
    rcon = [
        0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 
        0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 
        0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 
        0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 
        0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 
        0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 
        0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 
        0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 
        0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 
        0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 
        0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 
        0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 
        0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 
        0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 
        0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 
        0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb   
    ] 
    
    def key_expansion(self, key): # the key length has to be 16 !
        self.round_key = array.array('B', [0] * 176)
        #  the first round key is the key itself.
        for i in range(aes128.keylen):
            self.round_key[i] = ord(key[i])
        # all other round keys are found from the previous round keys
        for i in range(aes128.nk, aes128.nb * (aes128.nr + 1)):
            # take 4 subsequent bytes from the round key
            arr = array.array('B', [0] * aes128.nk)
            for j in range(aes128.nk):
                arr[j] = self.round_key[(i - 1) * 4 + j];
                
            if i % aes128.nk == 0:
                # rotate the 4 bytes in a word to the left once
                # [a0,a1,a2,a3] becomes [a1,a2,a3,a0]
                k = arr[0];
                arr[0] = arr[1];
                arr[1] = arr[2];
                arr[2] = arr[3];
                arr[3] = k;
                # take a four-byte input word and apply the S-box to 
                # each of the four bytes to produce an output word
                arr[0] = aes128.sbox[arr[0]];
                arr[1] = aes128.sbox[arr[1]];
                arr[2] = aes128.sbox[arr[2]];
                arr[3] = aes128.sbox[arr[3]];
                # xor with a round constant word
                arr[0] =  arr[0] ^ aes128.rcon[i / aes128.nk];
            # the each byte is xored with an respective byte from the previous word
            for j in range(aes128.nk):
                self.round_key[i * 4 + j] = self.round_key[(i - aes128.nk) * 4 + j] ^ arr[j]
       
    def add_round_key(self, block, round):
        for i in range(aes128.nk):
            for j in range(aes128.nk):
                block[i * aes128.nk + j] ^= self.round_key[round * aes128.nb * aes128.nk + i * aes128.nb + j]
    
    def inv_shift_rows(self, block):
        # rotate first row 1 columns to right  
        tmp                      = block[3 * aes128.nk + 1]
        block[3 * aes128.nk + 1] = block[2 * aes128.nk + 1]
        block[2 * aes128.nk + 1] = block[1 * aes128.nk + 1]
        block[1 * aes128.nk + 1] = block[0 * aes128.nk + 1]
        block[0 * aes128.nk + 1] = tmp
        # rotate second row 2 columns to right 
        tmp                      = block[0 * aes128.nk + 2]
        block[0 * aes128.nk + 2] = block[2 * aes128.nk + 2]
        block[2 * aes128.nk + 2] = tmp

        tmp                      = block[1 * aes128.nk + 2]        
        block[1 * aes128.nk + 2] = block[3 * aes128.nk + 2]
        block[3 * aes128.nk + 2] = tmp
        
        # rotate third row 3 columns to right
        tmp                      = block[0 * aes128.nk + 3]
        block[0 * aes128.nk + 3] = block[1 * aes128.nk + 3]
        block[1 * aes128.nk + 3] = block[2 * aes128.nk + 3]
        block[2 * aes128.nk + 3] = block[3 * aes128.nk + 3]
        block[3 * aes128.nk + 3] = tmp

    def shift_rows(self, block):
        # rotate first row 1 columns to left  
        tmp                      = block[0 * aes128.nk + 1]
        block[0 * aes128.nk + 1] = block[1 * aes128.nk + 1]
        block[1 * aes128.nk + 1] = block[2 * aes128.nk + 1]
        block[2 * aes128.nk + 1] = block[3 * aes128.nk + 1]
        block[3 * aes128.nk + 1] = tmp
        # rotate second row 2 columns to left  
        tmp                      = block[0 * aes128.nk + 2]
        block[0 * aes128.nk + 2] = block[2 * aes128.nk + 2]
        block[2 * aes128.nk + 2] = tmp

        tmp                      = block[1 * aes128.nk + 2]        
        block[1 * aes128.nk + 2] = block[3 * aes128.nk + 2]
        block[3 * aes128.nk + 2] = tmp

        # rotate third row 3 columns to left
        tmp                      = block[0 * aes128.nk + 3]
        block[0 * aes128.nk + 3] = block[3 * aes128.nk + 3]
        block[3 * aes128.nk + 3] = block[2 * aes128.nk + 3]
        block[2 * aes128.nk + 3] = block[1 * aes128.nk + 3]
        block[1 * aes128.nk + 3] = tmp

    def inv_sub_bytes(self, block):
        for i in range(aes128.nk):
            for j in range(aes128.nk):
                block[j * aes128.nk + i] = aes128.rsbox[block[j * aes128.nk + i]]
                
    def sub_bytes(self, block):
        for i in range(aes128.nk):
            for j in range(aes128.nk):
                block[j * aes128.nk + i] = aes128.sbox[block[j * aes128.nk + i]]

    # mixes the columns of the data matrix
    # the method used to multiply may be difficult to understand for the inexperienced
    # please use the references to gain more information
    def inv_mix_columns(self, block):
        for i in range(aes128.nk):
            a = block[i * aes128.nk + 0]
            b = block[i * aes128.nk + 1]
            c = block[i * aes128.nk + 2]
            d = block[i * aes128.nk + 3]
            
            block[i * aes128.nk + 0] = multiply(a, 0x0e) ^ multiply(b, 0x0b) ^ multiply(c, 0x0d) ^ multiply(d, 0x09)
            block[i * aes128.nk + 1] = multiply(a, 0x09) ^ multiply(b, 0x0e) ^ multiply(c, 0x0b) ^ multiply(d, 0x0d)
            block[i * aes128.nk + 2] = multiply(a, 0x0d) ^ multiply(b, 0x09) ^ multiply(c, 0x0e) ^ multiply(d, 0x0b)
            block[i * aes128.nk + 3] = multiply(a, 0x0b) ^ multiply(b, 0x0d) ^ multiply(c, 0x09) ^ multiply(d, 0x0e)
            
    # mix_columns function mixes the columns of the state matrix
    def mix_columns(self, block):
        for i in range(aes128.nk):
            t   = block[i * aes128.nk + 0]
            tmp = block[i * aes128.nk + 0] ^ block[i * aes128.nk + 1] ^ block[i * aes128.nk + 2] ^ block[i * aes128.nk + 3]
            
            tm = block[i * aes128.nk + 0] ^ block[i * aes128.nk + 1]
            tm = xtime(tm)
            block[i * aes128.nk + 0] ^= 0xFF & (tm ^ tmp)
            
            tm = block[i * aes128.nk + 1] ^ block[i * aes128.nk + 2]
            tm = xtime(tm)
            block[i * aes128.nk + 1] ^=  0xFF & (tm ^ tmp)

            tm = block[i * aes128.nk + 2] ^ block[i * aes128.nk + 3]
            tm = xtime(tm)
            block[i * aes128.nk + 2] ^= 0xFF & (tm ^ tmp) 

            tm = block[i * aes128.nk + 3] ^ t
            tm = xtime(tm)
            block[i * aes128.nk + 3] ^= 0xFF & (tm ^ tmp)

    def inv_cipher(self, block):
        # add the first round key to the state before starting the rounds
        self.add_round_key(block, aes128.nr) 
        # there will be nr rounds
        # the first nr-1 rounds are identical
        # these nr-1 rounds are executed in the loop below
        for round in reversed(range(1, aes128.nr)):
            self.inv_shift_rows(block);
            self.inv_sub_bytes(block);
            self.add_round_key(block, round)
            self.inv_mix_columns(block);
        # the last round is given below
        # the mix_columns function is not here in the last round
        self.inv_shift_rows(block);
        self.inv_sub_bytes(block);
        self.add_round_key(block, 0)
        # bytes to chars
        return block
    
    def cipher(self, block):
        # add the first round key to the state before starting the rounds
        self.add_round_key(block, 0)
        # there will be nr rounds.
        # the first nr-1 rounds are identical
        # these nr-1 rounds are executed in the loop below
        for round in range(1, aes128.nr):
            self.sub_bytes(block)      
            self.shift_rows(block)  
            self.mix_columns(block)
            self.add_round_key(block, round)
        # the last round is given below
        # the mix_ Columns function is not here in the last round
        self.sub_bytes(block)      
        self.shift_rows(block)  
        self.add_round_key(block, aes128.nr)
        # bytes to chars
        return block
        
    def decrypt_ecb(self, txt, key):
        self.key_expansion(key)
        ret = array.array('B', [])
        remainder = len(txt) % aes128.keylen;
        for i in  range(len(txt) / aes128.keylen):
            block = array.array('B', txt[i * aes128.keylen : (i + 1) * aes128.keylen])
            ret += self.inv_cipher(block)
        # handle reminder
        if remainder > 0:
            i = len(txt) / aes128.keylen
            block = array.array('B', txt[i * aes128.keylen : i * aes128.keylen + remainder])
            #padding
            block.extend([0] * (aes128.keylen - remainder))
            ret += self.inv_cipher(block)
        # return the encrypted string            
        return "".join(chr(b) for b in ret)
    
    def encrypt_ecb(self, txt, key):
        self.key_expansion(key)
        ret = array.array('B', [])
        remainder = len(txt) % aes128.keylen;
        for i in  range(len(txt) / aes128.keylen):
            block = array.array('B', txt[i * aes128.keylen : (i + 1) * aes128.keylen])
            ret += self.cipher(block)
        # handle reminder
        if remainder > 0:
            i = len(txt) / aes128.keylen
            block = array.array('B', txt[i * aes128.keylen : i * aes128.keylen + remainder])
            #padding
            block.extend([0] * (aes128.keylen - remainder))
            ret += self.cipher(block)
        # return the encrypted string                 
        return "".join(chr(b) for b in ret)
    
    def decrypt_cbc(self, txt, key, iv):
        self.key_expansion(key)        
        ret = array.array('B', [])
        iv_arr = array.array('B', iv)
        remainder = len(txt) % aes128.keylen;
        for i in  range(len(txt) / aes128.keylen):
            block = array.array('B', txt[i * aes128.keylen : (i + 1) * aes128.keylen])
            block = self.inv_cipher(block)
            ret += xor_bytes(block, iv_arr)
            iv_arr = array.array('B', txt[i * aes128.keylen : (i + 1) * aes128.keylen])
        # handle reminder
        if remainder > 0:
            i = len(txt) / aes128.keylen
            block = array.array('B', txt[i * aes128.keylen : i * aes128.keylen + remainder])
            #padding
            block.extend([0] * (aes128.keylen - remainder))
            block = self.inv_cipher(block)
            ret += xor_bytes(block, iv_arr)       
        # return the decryptet string
        return "".join(chr(b) for b in ret)
    
    def encrypt_cbc(self, txt, key, iv):
        self.key_expansion(key)        
        ret = array.array('B', [])
        iv_arr = array.array('B', iv)
        remainder = len(txt) % aes128.keylen;
        for i in  range(len(txt) / aes128.keylen):
            block = array.array('B', txt[i * aes128.keylen : (i + 1) * aes128.keylen])
            block = xor_bytes(block, iv_arr)
            ret += self.cipher(block)
            iv_arr = array.array('B', ret[i * aes128.keylen : (i + 1) * aes128.keylen])
        # handle reminder
        if remainder > 0:
            i = len(txt) / aes128.keylen
            block = array.array('B', txt[i * aes128.keylen : i * aes128.keylen + remainder])
            #padding
            block.extend([0] * (aes128.keylen - remainder))
            block = xor_bytes(block, iv_arr)
            ret += self.cipher(block)
        # return the encrypted string
        return "".join(chr(b) for b in ret)
    

def get_text():
    response = urllib2.urlopen('http://cryptopals.com/static/challenge-data/10.txt')
    return base64.b64decode(response.read())

if __name__ == '__main__':
    txt = get_text()
    key = 'YELLOW SUBMARINE'
    iv = [0] * 16
    d = aes128()
    print d.decrypt_cbc(txt, key, iv)
 
    
    
