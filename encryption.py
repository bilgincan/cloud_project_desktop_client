import hashlib
from random import seed
from random import random
from Crypto.Cipher import AES
from Crypto import Random
import base64
from Crypto.Hash import MD5

bs = AES.block_size
def generate_key():
    random_number = str(random()*1500)
    m = hashlib.sha1()
    m.update((random_number).encode())
    key = m.digest()
    return key

def _pad(s):
    return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

def _unpad(s):
    return s[:-ord(s[len(s)-1:])]

def encrypt(key,raw):
    key = MD5.new(str(key).encode()).digest()
    raw = _pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw.encode()))

def decrypt(key, enc):
    key = MD5.new(str(key).encode()).digest()
    enc = base64.b64decode(enc)
    iv = enc[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return _unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

def simple_encrypt(key,message,lucky_number):
    cipher = ""
    for i in range(len(message)):
        encrypted = ord(key[i]) ^ ord(message[i]) ^ lucky_number
        cipher += chr(encrypted)
    return cipher

def simple_decrypt(key,cipher, lucky_number):
    message = ""
    for i in range(len(cipher)):
        decrypted = ord(key[i]) ^ ord(cipher[i]) ^ lucky_number
        message += chr(decrypted)
    return message

def RSA_encrypt(message, key):
    return pow(message,key.e) % key.n

def RSA_decrypt(cipher, key):
    return pow(cipher,key.d) % key.n
