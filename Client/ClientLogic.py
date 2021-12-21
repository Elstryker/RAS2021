import socket
from ClientGUI import *

class ClientLogic:
    
    sock : socket.socket

    def __init__(self,sock):
        self.sock = sock

    def menu(self):
        inp = ''
        while inp != '0':
            ClientGUI.show_Menu()
            inp = input(" -> ")
            # try:
            option = int(inp)
            message = self.handleInput(option)
            data = message.encode('utf-8')
            self.sock.send(data)
            data = self.sock.recv(256)
            print(data.decode("utf-8"))
            # except:
            #     print("Not a valid option")

    def handleInput(self,option):
        message = ""
        if option == 1:
            ClientGUI.deposit_money()
            amount = input("-> ")
            message = str(option) + " " + amount

        elif option == 0:
            message = '0'

        return message

    
    def run(self):
        self.menu()
        self.closeConnection()

    def closeConnection(self):
        self.sock.close()
