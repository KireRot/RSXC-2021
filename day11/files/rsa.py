from Crypto.PublicKey import RSA #pycryptodome
from Crypto.Cipher import PKCS1_OAEP
from sympy import randprime, nextprime, invert
import base64

p = randprime(2**1023, 2**1024)
q = nextprime(p*p)

n = p*q
e = 65537

phi = (p-1)*(q-1)
d = int(invert(e,phi))

key = RSA.construct((n,e,d,p,q))
rsa = PKCS1_OAEP.new(key)

print(n)
print()
print(base64.b64encode(rsa.encrypt(open('./flag.txt','rb').read())).decode("ascii"))
