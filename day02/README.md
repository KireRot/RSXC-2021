# Day 2 - A magic word
We have found a magical port that is listening on port 20002, maybe you can find todays flag there?
rsxc.no:20002

## Write-Up
Today we are given both server and port. If we try to connect to it with netcat or firefox we are only recieving a message telling us **"That is not the byte I want!"**.

So the server wants a byte. A byte could be many things, but the first that comes to mind that we should try first is bytes from **00** to **ff**.

After a couple of lines of code...

``` python
import socket

for i in range(256):
    h = hex(i)[2:].zfill(2)
    print(h)
    buf = bytes.fromhex(h)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("rsxc.no", 20002))
    s.send(buf)
    msg = s.recv(1024)
    s.close()

    if not msg.startswith(b'That is not the byte I want!'):
        print(msg.decode('utf-8'))
        break
```

When running the script we get the following output.

``` shell
d4
RSXC{You_found_the_magic_byte_I_wanted_Good_job!}
```

## The Flag
RSXC{You_found_the_magic_byte_I_wanted_Good_job!}