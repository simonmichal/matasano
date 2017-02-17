
import base64
from challenge10 import aes128

def parse_cookie( cookie ):
    return dict( p.split( '=' ) for p in cookie.split( '&' ) )

def encrypt( profile ):
    random_key = 'YHcTTdBjsPeoGOag'
    enc = aes128()
    return enc.encrypt_ecb(profile, random_key)

def profile_for( email ):
    d = { 'email' : email.translate( None, '=&' ), 'uid' : 10, 'role' : 'user' }
    profile = '&'.join( [ str( i[0] ) + '=' + str( i[1] ) for i in d.items() ] )
    return encrypt( profile )

if __name__ == '__main__':
    profile = profile_for( 'lolek.baca@host.d.edu' )
    print profile
    