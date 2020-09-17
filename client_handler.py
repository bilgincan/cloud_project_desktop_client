import socket
from encryption import encrypt, decrypt

HOST = '127.0.0.1'
PORT = 8787

def handshaking_protocol():
    s.send(("key").encode())
    key = s.recv(4096).decode()

    user_name = encrypt(key, "cnblgn", 0)
    password = encrypt(key, "unicorn", 42)

    user_data = user_name + " , " + password

    s.send(user_data.encode())
    print(s.recv(1024))
    s.close()
    exit()

s = socket.socket()
s.connect((HOST, PORT))

accepted = s.recv(1024).decode()
if accepted == "Connection accepted\n":
    handshaking_protocol()
else:
    s.close()
