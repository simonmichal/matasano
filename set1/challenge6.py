'''
Created on 3 Oct 2014

@author: simonm
'''

import bitarray
import urllib2
import base64
import array
import re
from itertools import cycle
from math import sqrt
from sys import float_info

def to_bitarray(string):
    ba = bitarray.bitarray()
    ba.fromstring(string)
    return ba

def hamming_distance(str1, str2):
    return sum(1 for (b1, b2) in zip(to_bitarray(str1), to_bitarray(str2)) if b1 != b2)

def guess_key_size(txt):
    # return the key size with minimum normalised distance 
    # (start assuming maximum)
    ret = 0, 8.0
    # try key sizes in range 2 to 40
    for size in range(2, 41) :
        # take 4 blocks of size i
        blocks = [txt[size * j : size * (j + 1)] for j in range(0, 4)]
        # generate all possible pair (without repetitions)
        all_pairs = [(x, y) for i, x in enumerate(blocks) for j, y in enumerate(blocks) if x != y and i < j]
        # calculate the average hamming_distance, and normalise
        avg = sum(map(lambda pair: hamming_distance(*pair), all_pairs)) / float(len(all_pairs)) / float(size)
        # pick the smallest average distance
        if avg < ret[1]: ret = size, avg
    return ret[0]

def get_text():
    response = urllib2.urlopen('http://cryptopals.com/static/challenge-data/6.txt')
    return response.read()

def to_columns(txt, key_size):
    # as many entries as we expect columns
    columns = [''] * key_size
    # start with index 0
    index = 0
    # group the chars into key_size columns
    for char in txt:
        columns[index] += char
        index = (index + 1) % key_size
    return columns

def rate_string(string):
    # first make sure it contains only valid characters
    if not re.match(r"^[\n\w '-?!.,:;()&]+$", string): return float_info.max
    # now let's check how much the string varies from expectations
    # expected ratios for all characters (according to Wikipedia ;)
    expected = {
          'a' : 0.08167, 'b' : 0.01492, 'c' : 0.02782, 'd' : 0.04253,     
          'e' : 0.12702, 'f' : 0.02228, 'g' : 0.02015, 'h' : 0.06094,     
          'i' : 0.06966, 'j' : 0.00153, 'k' : 0.00772, 'l' : 0.04025,     
          'm' : 0.02406, 'n' : 0.06749, 'o' : 0.07507, 'p' : 0.01929, 
          'q' : 0.00095, 'r' : 0.05987, 's' : 0.06327, 't' : 0.09056,     
          'u' : 0.02758, 'v' : 0.00978, 'w' : 0.02360, 'x' : 0.00150,     
          'y' : 0.01974, 'z' : 0.00074
        }
    # now calculate the actual ratios in the string
    ratios = {}
    for char in expected.keys():
        ratios[char] = string.count(char) / float(len(string))
    # now calculate the standard deviation    
    stdev = 0
    for char in ratios.keys():
        stdev += (expected[char] - ratios[char]) ** 2
    stdev = sqrt(stdev / float(len(ratios)))

    return stdev;

def xor_str(txt, key):
    byte_arr = array.array('B', txt)
    key_arr  = array.array('B', key)
    result_arr = [b ^ k for b, k in zip(byte_arr, cycle(key_arr))]
    # translate each byte to ASCII
    return "".join(chr(b) for b in result_arr)

def try_chars(txt):
    ret = 0, float_info.max
    # try every character
    for i in range(0, 256):
        # decode string 
        string = xor_str(txt, [i])
        # rate it
        p = rate_string(string)
        # choose the one with highest rate
        if p < ret[1]: ret = i, p
    return chr(ret[0])

def get_key(txt, key_size):
    ret = ''
    # split the text into key_size columns
    columns = to_columns(txt, key_size)
    # for each column
    for column in columns:
        # try decoding with each character 
        # and choose the best one
        ret += try_chars(column)
    return ret;

if __name__ == '__main__':
    # make sure hamming_distance works properly
    print(hamming_distance('this is a test', 'wokka wokka!!!') == 37)
    # get the text and decode it
    txt = base64.b64decode(get_text())
    # guess the key size
    key_size = guess_key_size(txt)
    print('key size: ', key_size)
    # get the key
    key = get_key(txt, key_size)
    print('key: ', key)
    # xor the text against the key
    plain = xor_str(txt, key)
    print('plain text: ')
    print(plain)

                