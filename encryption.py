import hashlib
from random import seed
from random import random

def generate_key():
    random_number = str(random()*1500)
    m = hashlib.sha1()
    m.update((random_number).encode())
    key = m.digest()
    return key

def encrypt(key,message,lucky_number):
    cipher = ""
    for i in range(len(message)):
        encrypted = ord(key[i]) ^ ord(message[i]) ^ lucky_number
        cipher += chr(encrypted)
    return cipher

def decrypt(key,cipher, lucky_number):
    message = ""
    for i in range(len(cipher)):
        decrypted = ord(key[i]) ^ ord(cipher[i]) ^ lucky_number
        message += chr(decrypted)
    return message
