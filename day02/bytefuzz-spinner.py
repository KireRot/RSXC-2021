from progress.spinner import Spinner
import socket


# Running through all bytes as hex
spinner = Spinner('Processing ')

for i in range(256):
    h = hex(i)[2:].zfill(2)
    #print(h)

    sendbuf = bytes.fromhex(h)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("rsxc.no", 20002))
    s.send(sendbuf)
    msg = s.recv(1024)
    
    s.close()

    spinner.next()    
    if not msg.startswith(b'That is not the byte I want!'):
        print("\n")
        print("Byte found for Integer:", i, "Hex value:", hex(i))
        print(msg.decode('utf-8'))
        break

spinner.finish()