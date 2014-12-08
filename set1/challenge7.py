'''
Created on 12 Nov 2014

@author: simonm
'''

import urllib2
import base64
import M2Crypto

def get_decryptor(key, alg='aes_128_ecb', iv=None):
    if iv == None:
        iv = '\0' * 16
    cryptor = M2Crypto.EVP.Cipher(alg=alg, key=key, iv=iv, op=0)
    return cryptor

def get_text():
    response = urllib2.urlopen('http://cryptopals.com/static/challenge-data/7.txt')
    return response.read()

if __name__ == '__main__':
    data = base64.b64decode(get_text())
    decryptor = get_decryptor('YELLOW SUBMARINE')
    plain =  decryptor.update(data)
    plain += decryptor.final()
    print(plain)
