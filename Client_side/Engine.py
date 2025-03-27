from tkinter import *
from Client_side.Users_Registertion import Log_In, Register
from Client_side.App import App


class AppEngine:

    def __init__(self, client):
        self.window = Tk()
        height = 650
        width = 1240
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 4) - (height // 4)
        self.window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.window.resizable(False, False)
        self.window.configure(bg="#ffffff")
        self.status = ["Log_In"]
        self.client = client
        self.update_state()

    def update_state(self):
        print("state status: " + self.status[0])
        try:
            if self.status[0] == "Exit":
                self.exit()
            elif self.status[0] == "Log_In":
                state = Log_In.LogIn(self.window, self.status, self.client)
            elif self.status[0] == "Register":
                state = Register.Register(self.window, self.status, self.client)
            elif self.status[0] == "App":
                state = App.App(self.window, self.status, self.client)

        except Exception as e:
            self.client.logout()
            exit(1)
        self.update_state()

    def exit(self):
        self.client.logout()
        self.window.quit()
        print("exit successfully...")
        exit()




