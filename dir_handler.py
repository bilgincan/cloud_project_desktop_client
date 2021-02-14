import socket
import os
import tqdm
# from client_handler import login_procedure

BUFFER_SIZE = 4096

def receive_files_and_write(s, path):
    try:
        os.mkdir(path)
    except OSError:
        print(OSError)

    l = 1
    file_name = ""
    f = ""
    while(l):
        l = s.recv(BUFFER_SIZE)
        print(path)
        try:
            msg = l.decode()
            if "mkdirNcd" in msg:
                new_dir = msg.split("mkdirNcd ")[1]
                subdir = path +"/"+ new_dir
                receive_files_and_write(s, subdir)
                continue
            elif msg == "D6642D2FE679ED121CB9067EE0DC10C244CCAB926BCCD9D18C3021E66330384C":
                file_name = s.recv(BUFFER_SIZE).decode()
                f = open((path+"/"+file_name),"w+")
                print(file_name)
                print("new plain text")
                continue
            elif "cd .." in msg:
                return
            if f != "":
                f.write(msg)
        except (UnicodeDecodeError, TypeError):
            if f != "":
                f.close()
            f = open((path+"/"+file_name), "wb+")
            print("new binary file")
            while(l):
                if not f.closed:
                    f.write(l)
                l = s.recv(BUFFER_SIZE)
                try:
                    msg = l.decode()
                    if msg == "db2350b264d0b0a4b14528c94dbfaf7ef7cc90a525062bb39f5eba3093e9e095":
                        break
                    if msg == "D6642D2FE679ED121CB9067EE0DC10C244CCAB926BCCD9D18C3021E66330384C":
                        f.close()
                        file_name = s.recv(BUFFER_SIZE).decode()
                        print(file_name)
                        f = open((path+"/"+file_name),"w+")
                        break
                    elif "cd .." in msg:
                        return
                    elif "mkdirNcd" in msg:
                        new_dir = msg.split("mkdirNcd ")[1]
                        subdir = path +"/"+ new_dir
                        receive_files_and_write(s, subdir)
                        continue
                except UnicodeDecodeError:
                    continue
        except IsADirectoryError:
            s.close()
            return 1

        print("aldı")
    #s.send("received".encode())
    s.close()
    print("socket has been closed")
    if f != "":
        f.close()
    return 0
