from pwn import *
import base64
import time

#Connect with netcat 
io = connect("rsxc.no", 20012) 
 
#Recieve data
data = io.recvline().decode()
print(data)

start = time.time()
#Recieve the taskline containing the task
for i in range(102):
    taskline = io.recvline().decode().strip()
    print ("[ Time:",format(((time.time())-start), ".2f"),"- Task:",i+1,"] Task:", taskline)

    #HEX Decode
    if "hex" in taskline:
        hexstr = taskline.split(": ")[1]
        decoded = bytes.fromhex(hexstr)
        # print(decoded)
        io.sendline(decoded.decode('ascii').encode())

    # Base64 Decode
    elif "base64" in taskline:
        encoding = taskline.split(": ")[1]
        decoded = base64.b64decode(encoding)
        # print(decoded)
        io.sendline(decoded)

    # String Reverse
    elif "reverse this string" in taskline:
        str = taskline.split(": ")[1]
        revstr = str[::-1]
        # print(revstr)
        io.sendline(revstr.encode())

    # String Lower
    elif "lower case" in taskline:
        str = taskline.split(": ")[1]
        # print(str.lower())
        io.sendline(str.lower().encode())
    
    # No Task - Flag?
    else:
        print("\n[+]",taskline,"\n")
        break

io.close()