import socket
import os
import tqdm

BUFFER_SIZE = 4096

def receive_files_and_write(s, user_name):
    try:
        os.mkdir(user_name)
    except OSError:
        print(OSError)

    l = 1
    file_name = ""
    while(l):
        l = s.recv(BUFFER_SIZE)
        try:
            if l.decode() == "D6642D2FE679ED121CB9067EE0DC10C244CCAB926BCCD9D18C3021E66330384C":
                file_name = s.recv(BUFFER_SIZE).decode()
                f = open((user_name+"/"+file_name),"w+")
                print("new plain text")
                continue
            f.write(l.decode())
        except (UnicodeDecodeError, TypeError):
            f.close()
            f = open((user_name+"/"+file_name), "wb+")
            print("new binary file")
            while(l):
                f.write(l)
                l = s.recv(BUFFER_SIZE)
                try:
                    if l.decode() == "D6642D2FE679ED121CB9067EE0DC10C244CCAB926BCCD9D18C3021E66330384C":
                        f.close()
                        file_name = s.recv(BUFFER_SIZE).decode()
                        f = open((user_name+"/"+file_name),"w+")
                        break
                except UnicodeDecodeError:
                    continue

        print("aldı")

    f.close()
    s.send("received".encode())
    # s.close()
    # exit()
