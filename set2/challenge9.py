'''
Created on 18 Nov 2014

@author: simonm
'''

def padd_pkcs7(str, n):
    
    r = len(str) % n
    for i in range(n - r):
        str += chr(0x4)
    return str

if __name__ == '__main__':
    str = "YELLOW SUBMARINE"
    res = "YELLOW SUBMARINE\x04\x04\x04\x04"
    str = padd_pkcs7(str, 20)
    print(str == res)
