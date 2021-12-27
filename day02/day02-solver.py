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