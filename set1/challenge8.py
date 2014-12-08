'''
Created on 18 Nov 2014

@author: simonm
'''

import urllib2
from os.path import commonprefix

def longest_duplicate(txt):
    sufixarr = [buffer(txt, i) for i in range(len(txt))]
    sufixarr.sort()
    ret = ''
    for i in range(1, len(sufixarr)): 
        prefix = commonprefix([sufixarr[i - 1], sufixarr[i]])
        if len(prefix) > len(ret) : ret = prefix
    return ret
    

def is_aes_ecb(txt):
    if len(longest_duplicate(txt)) == 16: return True
#     for i in range(len(txt) - 16 + 1):
#         substr = txt[i : i + 16]
#         if txt.count(substr) > 1 : return True
    return False

def get_text():
    response = urllib2.urlopen('http://cryptopals.com/static/challenge-data/8.txt')
    return response.read()

if __name__ == '__main__':
    hexlines = get_text().splitlines()
    lines = []
    for hexstr in hexlines:
        txt = hexstr.decode('hex')
        if (is_aes_ecb(txt)): print(hexstr)

