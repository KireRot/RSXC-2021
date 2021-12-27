# Day 4 - 4 Bytes of XOR
The flag of the day can be found by xor'ing our text with 4 bytes.

## Write-UP
As usual we start by looking at the contents of the given link and find some kind of scrambled text

```
0xda0x960x0c0x960xf30x880x3b0xa60xfc0x9a0x230xba0xfd0xa90x300x8a0xfb0xa40x2d0x8a0xd00x8a0x060x8a0xe10xb60x
3a0xf20xfc0x9a0x200xbd0xe90xb10x0b0xa00xfb0xa00x320xa00xe40x9a0x350xbb0xf10xa80x3b0xa70xed0xb8
```

At first I stared at this and could not see what I needed. We ware given hints about "4 Bytes of XOR", which should indicate that we need to find a "key" of 4 bytes that we need to XOR with the given text. My problem was that I could not see that this string is a string of hex values prepended with `0x`... When I cleared my glasses and saw it I thought the solution should be kinda easy. The only minor problem is to validate the key.

We are given a ChiperText and know that a `Message` has been `XOR'ed` with it to give this text. Knowing how `XOR` works, we also know that taking the `CipherText` and XOR-ing it with the Key will give us the `Message`. For the message we could guess that the first 4 characters are `RSXC` as this is the start of the Flag we are after.

This was the path I wanted to go and started on a Python script to solve this for me. This is the code result. (My python programming is a bit rusty, so there is probably easier ways to program this)

```python
### Day04 - Decrypter - 4 Bytes of XOR

# Given string - CipherText - ct
ct = '0xda0x960x0c0x960xf30x880x3b0xa60xfc0x9a0x230xba0xfd0xa90x300x8a0xfb0xa40x2d0x8a0xd00x8a0x060x8a0xe1
0xb60x3a0xf20xfc0x9a0x200xbd0xe90xb10x0b0xa00xfb0xa00x320xa00xe40x9a0x350xbb0xf10xa80x3b0xa70xed0xb8'

# Split into list of hex strings
n = 4
hexlist = [ct[i:i+n] for i in range(0, len(ct), n)]

# Need list for possible key
keylist = []

# Guessing Clear Text will start with "RSXC" as the first 4 characters
cleartext = ['R', 'S', 'X', 'C']

# Find possible Key
for i in range(4):
    for x in range(256):
        if cleartext[i] == ( chr( (int(hexlist[i], 16) ^ x) ) ):
            #print("Key Found " * 5)
            keylist.append(x)
            break

print("Possible Key (dec) found:", keylist[0], keylist[1], keylist[2], keylist[3])
print("Possible Key (hex) found:", hex(keylist[0]),hex(keylist[1]),hex(keylist[2]),hex(keylist[3]))

# Clear Text Message
message = []

# Decrypt CT
for i in range(len(hexlist)):
    char = ( chr( (int(hexlist[i], 0) ^ keylist[i%4] ) ) ) 
    message.append(char)

print("\nIf all is right, the Flag should be: ", "".join(message) )
```

Running the script solves the challenge

```python
$ python3 day04-decrypter.py
Possible Key (dec) found: 136 197 84 213
Possible Key (hex) found: 0x88 0xc5 0x54 0xd5

If all is right, the Flag should be:  RSXC{Most_would_say_XOR_isn't_that_useful_anymore}
```

## Write-Up - Alternative
During my communications with [Google](https://google.com) I came across an online decrypter that could solve such challenges for us; [XOR Cipher](https://www.dcode.fr/xor-cipher). Inputing the CipherText and that we knoe the key is 4 bytes and the result should be "Ascii (Printable) Characters", we get possible solutions where one of the first shows us the key, `88c554d5` and the message, `RSXC{Most_would_say_XOR_isn't_that_useful_anymore}`.

## The Flag
RSXC{Most_would_say_XOR_isn't_that_useful_anymore}
