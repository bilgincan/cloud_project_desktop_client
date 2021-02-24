from tkinter import *
from encryption import *

class Login:
    def __init__(self, message):
        self.main_screen = Tk()   # create a GUI window
        # create a Form label
        Label(text="CNBLGN BULUT SERVİSİNE HOŞGELDİNİZ", bg="orange", width="300", height="2", font=("Calibri", 13)).pack()
        # create Login Button
        Label(text=message, bg="red").pack()

        # login_screen = Toplevel(main_screen)
        # login_screen.title("Giriş yap")
        self.main_screen.geometry("450x250")

        self.username = StringVar()
        self.password = StringVar()

        username_label = Label(self.main_screen, text="Kullanıcı adı: ")
        username_label.pack()

        username_entry = Entry(self.main_screen, textvariable=self.username)
        username_entry.pack()

        password_label = Label(self.main_screen, text="Şifre: ")
        password_label.pack()

        password_entry = Entry(self.main_screen, textvariable=self.password, show="*")
        password_entry.pack()

        Label(text="").pack()
        Button(text="Giriş Yap", height="2", width="30", command=self.register).pack()
        self.main_screen.mainloop() # start the GUI

    def register(self):
        username_info = self.username.get()
        password_info = self.password.get()
        key = str(generate_key())
        password_info = simple_encrypt(key, password_info, 0)

        f = open("user_data.txt", "w+")
        f.write(key)
        f.write("\n")
        f.write(username_info)
        f.write("\n")
        f.write(password_info)

        self.main_screen.destroy()
