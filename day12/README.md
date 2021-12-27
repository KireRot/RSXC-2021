# Day 12 - Twelve seconds of encoding
For this challenge you need to do some encoding, but remember, you need to do it quickly, before the time runs out.

## Write-Up
It looks like we need to be QUICK to solve todays challenge... 12 seconds.

Opening the link in a browser just to look at what happens..

```
Good luck, you have 12 seconds to solve these 100 tasks!
Can you please hex decode this for me: 596e71486d4478574f42
No match
```

Looks like we are given 12 seconds to solve 100 tasks. First thing we should do is to connect to the port and see if the tasks are random and if they consist of different tasks.

Connecting a few times, tells us that there are random tasks and at least consist of

- Decode HEX
- Decode Base64
- Converting Strings to lowercase

```
$ nc rsxc.no 20012
Good luck, you have 12 seconds to solve these 100 tasks!
Can you please hex decode this for me: 674e5053744f7972
```

We will probably encounter other tasks, but it lines up what we need to do.

For this we can create a python script that connects, reads every task and solves it. As we only have 12 seconds to do it, we are not able to do this manually :D The info says there are 100 tasks to be completed, so guessing we are given the Flag after 100 correct solved taskes within the time limit.

Surely many possible solutions to this, but here the "50 lines of code" that solved it for me.

Minor remark... there actually are 101 tasks to complete... ;)

```py
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
```

Running the code and we get the flag

``` shell
[ Time: 4.21 - Task: 100 ] Task: Please reverse this string for me: CjBnpMFcHMw
[ Time: 4.25 - Task: 101 ] Task: Can you please hex decode this for me: 4d6f4255675156
[ Time: 4.29 - Task: 102 ] Task: RSXC{Seems_like_you_have_a_knack_for_encoding_and_talking_to_servers!}

[+] RSXC{Seems_like_you_have_a_knack_for_encoding_and_talking_to_servers!} 
```

## The Flag
RSXC{Seems_like_you_have_a_knack_for_encoding_and_talking_to_servers!}