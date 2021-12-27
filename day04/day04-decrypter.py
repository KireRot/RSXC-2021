### Day04 - Decrypter - 4 Bytes of XOR

# Given string - CipherText - ct
ct = '0xda0x960x0c0x960xf30x880x3b0xa60xfc0x9a0x230xba0xfd0xa90x300x8a0xfb0xa40x2d0x8a0xd00x8a0x060x8a0xe10xb60x3a0xf20xfc0x9a0x200xbd0xe90xb10x0b0xa00xfb0xa00x320xa00xe40x9a0x350xbb0xf10xa80x3b0xa70xed0xb8'

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
        #print("Testing x =", x)
        #print( chr( (int(hexlist[i], 0) ^ x) ) )
        if cleartext[i] == ( chr( (int(hexlist[i], 16) ^ x) ) ):
            #print("Key Found " * 5)
            keylist.append(x)
            break

print("Possible Key (dec) found:", keylist[0], keylist[1], keylist[2], keylist[3])
print("Possible Key (hex) found:", hex(keylist[0]),hex(keylist[1]),hex(keylist[2]),hex(keylist[3]))

message = []
# Decrypt CT
for i in range(len(hexlist)):
    char = ( chr( (int(hexlist[i], 0) ^ keylist[i%4] ) ) ) 
    message.append(char)

print("\nIf all is right, the Flag should be: ", "".join(message) )