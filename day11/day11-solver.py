from Crypto.PublicKey import RSA #pycryptodome
from Crypto.Cipher import PKCS1_OAEP
from sympy import randprime, nextprime, invert
import base64
import gmpy2

# From rsa.out we get...
# Guessing there was a redirect to rsa.out as the script was run...
# python3 rsa.py > rsa.out

# n value is the first printed
n = 1415732912633110850463082290910531310944025185851628960496687559483254746929720221647023240242336158686917844098726955123922281990353849950572386591304198809887980195592164437463694396551629025725893297740721210740603852117845187276240822110209890805395726319272811238182117091397934074647625229734002195089686974969651954470535554347943901878883362518072923354248859147416112318206824337487445716704648503565676180267966061851236231329358955557146660099270996351905681299543490284088388917086359028800783355214649085181453134992031245774041645632697445995388906670744100784647364712047823965135210709248854353892069782338755245211910680179291304283133858067808724881428158118018329116480623919406482183591009161012049808848921597384462762413755053792928218673793301012582611446447895722794852586858407955308203712823698883371297395149325161872495891941488144882598336487422503139931872453298083167787506759793770112004781589

# Second value is the cipher text.
# From the code, it is ciphertext, base64 encoded and 
# represented as ascii text instead of byte-string.
ascii64ct = "MybmIUY2CCSU7M6ojf6PjIXcECMBRgJRH1n1U15dB7L5VXgD4uC8Ry3U+isYpLlhEkw3HjmCTMjPM1trqON1eoV/ZGhtfQvK/iy/FdyAPmV6ykLofWBqFViMGtWebYRYqqKubbMux4aupS4uu2ppR+VIjqOBDuiMwqxvRzxGcRsc7vMGhi6F8qfBuiD+V1Kfe9MhhU1vxNb8a745qLSRc8wjIYQ4a4lPqy0H3dBPuoT3clR9A0dTvQsTq5kfUGBC072ij2RFpBBW9d2qj+KihLapaH6I1ZyZmmBFl83+Qb5QbM0RBB/wAfOKfZ3lfPoRpEjST9MX/J/RBvlaCPaqpkApNCr5bV/6rqxs+paN08bkvdQ5tapcSWR9jXuw+mY1RzS9sb7rbaBoVdwArEUyJwlUBoLiNxkE6w6NPgKpNpmQ08Tm8b1PK2CAs6TW9e6JphwpZlsy76BSpEJgFHLpeqNxmgAY1ESGfCx9soiv9KSPYMvDkm4JbmtH7GHqslzB"

# A Byte-Base64-CipherText
byte64ct = ascii64ct.encode('utf-8')

# Getting the CiperText needed
ct = base64.b64decode(byte64ct)

## Trying to guess p and q
r = gmpy2.iroot(n,3)
p = int(gmpy2.mpz(r[0]))

for padding in range (-100,100):
    cp = p + padding

    if n % cp == 0:
        print("[*] - Found Candidate P")
        print("[*] - Calcualte Candidate Q")
        cq = nextprime(cp*cp)

        if cp * cq == n:
            print("[*] - P & Q are found ---> Tested and verified")
            break

# Exponent known
e = 65537

phi = (cp-1)*(cq-1)
d = int(invert(e, phi))

key = RSA.construct((n,e,d,cp,cq))
rsa = PKCS1_OAEP.new(key)

print("[*] - Decrypting ciphetext:")
print("[*] -", (rsa.decrypt(ct)).decode('ascii'))