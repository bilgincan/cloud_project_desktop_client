import socket
from encryption import encrypt, decrypt
from login_gui import Login
from dir_handler import receive_files_and_write

HOST = '127.0.0.1'
PORT = 8787

def handshaking_protocol(s, user_name, password,count):
    s.send(("key").encode())
    key = s.recv(4096).decode()

    user_name_to_server = encrypt(key, user_name, 0)
    password_to_server = encrypt(key, password, 42)

    user_data = user_name_to_server + " , " + password_to_server

    s.send(user_data.encode())
    response = s.recv(1024).decode()
    if 'Unauthoritized: Wrong password or user name' in response and count < 2:
        Login("hatalı kullanıcı adı ya da şifre")
        login_procedure(count+1)
        response = s.recv(1024).decode()
        exit()

    print(response)
    s.send(("getall").encode())
    receive_files_and_write(s,user_name)
    exit()

def login_procedure(count):
    try:
        f = open("user_data.txt", "r")
    except:
        Login("")
        f = open("user_data.txt", "r")
    key = f.readline()[:-1]
    user_named = f.readline()[:-1]
    password = f.readline()
    password = decrypt(key, password, 0)

    s = socket.socket()
    s.connect((HOST, PORT))

    accepted = s.recv(1024).decode()
    if accepted == "Connection accepted\n":
        handshaking_protocol(s, user_named, password,count)
    else:
        s.close()

login_procedure(0)
