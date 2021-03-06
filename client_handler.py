import socket
import rsa
import base64
from Crypto.PublicKey.RSA import importKey
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import hashlib
from encryption import encrypt, decrypt, simple_encrypt, simple_decrypt
from login_gui import Login
from dir_handler import receive_files_and_write
from binascii import hexlify, unhexlify
import time
import random

HOST = '127.0.0.1'
PORT = 8787
f = open("server_pub_key", "r")
SERVER_PUB_KEY = importKey(f.read())
f.close()

f = open("priv_key")
PRV_KEY = importKey(f.read())
f.close()

DH_KEY = ""

def handshaking_protocol(s, user_name, password,count):
    global DH_KEY
    credentials = '{},{}'.format(user_name, password)
    credentials = bytes(credentials, "utf-8")
    cipher = SERVER_PUB_KEY.encrypt(credentials, 64)[0]
    base64txt = base64.b64encode(cipher)
    s.send(base64txt)

    received = base64.b64decode(s.recv(4128)).decode().split(",")
    print(received)

    message = received[0]
    signature = (int(received[1][1:]),)


    h = SHA256.new(message.encode()).digest()

    verification = SERVER_PUB_KEY.verify(h, signature)
    if verification == False:
        s.close()
    sign = PRV_KEY.sign(h, "")

    #DH parameters
    p = PRV_KEY.decrypt(int(received[3]))
    g = PRV_KEY.decrypt(int(received[4]))
    X = PRV_KEY.decrypt(int(received[5]))

    p = int(p)
    g = int(g)
    X = int(X)


    b = random.randint(0,p)
    Y = (g**b) % p

    print(p)
    print(g)
    print(X)
    print(Y)

    DH_KEY = SHA256.new(str( (X**b) % p).encode()).digest()
    print(base64.b64encode(DH_KEY))

    message = "{},{},{}".format(message, sign, Y)
    base64txt = base64.b64encode(message.encode())
    s.send(base64txt)

    response = s.recv(1024).decode()
    if 'Unauthoritized: Wrong password or user name' in response and count < 2:
        Login("hatalı kullanıcı adı ya da şifre")
        login_procedure(count+1)
        response = s.recv(1024).decode()
        exit()

    print(response)
    message = "getall"
    cipher = encrypt(DH_KEY, message)
    s.send(cipher)
    response = receive_files_and_write(s,user_name, DH_KEY)
    if response == 1:
        login_procedure(0)
    else:
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
    password = simple_decrypt(key, password,0)

    s = socket.socket()
    s.connect((HOST, PORT))

    accepted = s.recv(1024).decode()
    if accepted == "Connection accepted\n":
        handshaking_protocol(s, user_named, password,count)
    else:
        s.close()

login_procedure(0)
