'''
Created on 2 Oct 2014

@author: simonm
'''

import urllib2
from challenge3 import print_decoded

if __name__ == '__main__':
    response = urllib2.urlopen('http://cryptopals.com/static/challenge-data/4.txt')
    
    line = response.readline().strip()
    while line:
        print_decoded(line)
        line = response.readline().strip()
