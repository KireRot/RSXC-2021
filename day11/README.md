# Day 11 - The not so random prime

We intercepted some traffic from a malicious actor. They seemed to be using a not so secure implementation of RSA, could you help us figure out how they did it?

## Write-Up
The challenge for today is some RSA crypto. We start downloading the provide zip file for the challenge and verify that it actually is a zip file before we `unzip` the file :) We are given two files; `rsa.out` and `rsa.py`

I do not remember RSA crypto in detail, but the basics should be easy.
There need to be selected two primes (rather big), called *p* and *q*. From these primes we calculate *n = p \* q*. We also has to selct an integer for the exponent, *e*. This is usually chosen to be **65537**. All other needed values are calculated by using *p*, *q* and *e*. There are a lot more criterias to the crypto, but not needed here... bedtime-story: https://en.wikipedia.org/wiki/RSA_(cryptosystem)

The `rsa.out` contains two blocks of data.. The first looks to be a very large integer value, and the second looks to be a cipher text of some sorts..

Looking at the `rsa.py` and we have the implementation used, it seems... 

```py
 1	from Crypto.PublicKey import RSA #pycryptodome
 2	from Crypto.Cipher import PKCS1_OAEP
 3	from sympy import randprime, nextprime, invert
 4	import base64
 5	
 6	p = randprime(2**1023, 2**1024)
 7	q = nextprime(p*p)
 8	
 9	n = p*q
10	e = 65537
11	
12	phi = (p-1)*(q-1)
13	d = int(invert(e,phi))
14	
15	key = RSA.construct((n,e,d,p,q))
16	rsa = PKCS1_OAEP.new(key)
17	
18	print(n)
19	print()
20	print(base64.b64encode(rsa.encrypt(open('./flag.txt','rb').read())).decode("ascii"))
```

Line 18-20 is the output of the given `Python` script and from this we can make the assumption that the `rsa.out` actually is the output from running this script. Then we have *n* and the *encrypted text* for the file *flag.txt*. This file they have not given us... Bummer!

We have to decrypt the message, so making a decryption script. But first we need to find all the needed info. *n* is known, so we "only" need to find *p* and *q*.
Line 6-7 tells us how these numbers are selected.

*p* is a randomly selected prime, in a quite narrow range. But this should be OK. The Prime is random and large.

Selecting *q* seems to be the issue. `nextprime()` only selects the next prime of a given number, which in our case is *p\*p*.

If *p* = $x$, then *q* is close to $x^2$. 

From *n = p \* q*, we the can say that *n = $x$ \* $x^2$ = $x^3$*.

Knowing this we can try to find a suited value for *p* by calcualting *x = $\sqrt[3]{n}$*. This value of *p* will probably not be exactly correct, so we should do our calculations with a candidate *p*, *cp = (p + padding)* and *-100 < padding < 100*. If this does not result in finding *p* and *q* we should increase *padding*.

To test our Candidate P and Q we find from the RSA math, that *n mod cp == 0* for a valid *p*. From there we can calculate the rest as we know how *q* was selected in the implementation.

Wipping out some `python` script, results in the following

```py
from Crypto.PublicKey import RSA #pycryptodome
from Crypto.Cipher import PKCS1_OAEP
from sympy import randprime, nextprime, invert
import base64
import gmpy2

# From rsa.out we get...
# Guessing there was a redirect to rsa.out as the script was run...
# python3 rsa.py > rsa.out

# n value is the first printed
n = 141573291263311085046308229091053131094402518585162896049668755948325474692972022164702324024233615868
6917844098726955123922281990353849950572386591304198809887980195592164437463694396551629025725893297740721
2107406038521178451872762408221102098908053957263192728112381821170913979340746476252297340021950896869749
6965195447053555434794390187888336251807292335424885914741611231820682433748744571670464850356567618026796
6061851236231329358955557146660099270996351905681299543490284088388917086359028800783355214649085181453134
9920312457740416456326974459953889066707441007846473647120478239651352107092488543538920697823387552452119
1068017929130428313385806780872488142815811801832911648062391940648218359100916101204980884892159738446276
2413755053792928218673793301012582611446447895722794852586858407955308203712823698883371297395149325161872
495891941488144882598336487422503139931872453298083167787506759793770112004781589

# Second value is the cipher text.
# From the code, it is ciphertext, base64 encoded and 
# represented as ascii text instead of byte-string.
ascii64ct = "MybmIUY2CCSU7M6ojf6PjIXcECMBRgJRH1n1U15dB7L5VXgD4uC8Ry3U+isYpLlhEkw3HjmCTMjPM1trqON1eoV/ZGhtf
QvK/iy/FdyAPmV6ykLofWBqFViMGtWebYRYqqKubbMux4aupS4uu2ppR+VIjqOBDuiMwqxvRzxGcRsc7vMGhi6F8qfBuiD+V1Kfe9MhhU1
vxNb8a745qLSRc8wjIYQ4a4lPqy0H3dBPuoT3clR9A0dTvQsTq5kfUGBC072ij2RFpBBW9d2qj+KihLapaH6I1ZyZmmBFl83+Qb5QbM0RB
B/wAfOKfZ3lfPoRpEjST9MX/J/RBvlaCPaqpkApNCr5bV/6rqxs+paN08bkvdQ5tapcSWR9jXuw+mY1RzS9sb7rbaBoVdwArEUyJwlUBoL
iNxkE6w6NPgKpNpmQ08Tm8b1PK2CAs6TW9e6JphwpZlsy76BSpEJgFHLpeqNxmgAY1ESGfCx9soiv9KSPYMvDkm4JbmtH7GHqslzB"

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

```

Running this gives us our flag!

```shell
$ python3 rsxc11-solver.py
[*] - Found Candidate P
[*] - Calcualte Candidate Q
[*] - P & Q are found ---> Tested and verified
[*] - Decrypting ciphetext:
[*] - RSXC{Good_Job!I_see_you_know_how_to_do_some_math_and_how_rsa_works}
```

## The Flag
RSXC{Good_Job!I_see_you_know_how_to_do_some_math_and_how_rsa_works}