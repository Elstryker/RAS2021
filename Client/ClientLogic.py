import socket
from ClientGUI import *
class ClientLogic:
    
    sock : socket.socket
    availableCurrencies : list

    def __init__(self,sock,currencies):
        self.sock = sock
        self.availableCurrencies = currencies

    def menu(self):
        inp = ''
        while inp != '0':
            ClientGUI.showMenu()
            inp = input(" -> ")
            option = int(inp)
            message = self.handleInput(option)
            data = message.encode('utf-8')
            self.sock.send(data)
            data = self.sock.recv(256)
            print(data.decode("utf-8"))

    def handleInput(self,option):
        args = []
        separator = " "
        option = str(option)

        if option == "1": # Add Bet To Bet Slip
            ClientGUI.askEvent()
            eventID = input("-> ")
            ClientGUI.showDetailedEvent()
            result = input("-> ")
            args = [option,eventID,result]
        elif option == "2": # Remove Bet From Bet Slip
            ClientGUI.askEvent()
            eventID = input("-> ")
            args = [option,eventID]
        elif option == "3": # Cancel Bet Slip
            args = [option]
        elif option == "4": # Show Bet Slip
            args = [option]
        elif option == "5": # Deposit Money
            ClientGUI.askAmount()
            amount = input("-> ")
            currency = ''
            ClientGUI.askCurrency(self.availableCurrencies)
            currency = input("-> ")
            currency = self.availableCurrencies[int(currency)-1]
            args = [option,currency,amount]
        elif option == "6": # Withdraw Money
            ClientGUI.askAmount()
            amount = input("-> ")
            currency = ''
            ClientGUI.askCurrency(self.availableCurrencies)
            currency = input("-> ")
            currency = self.availableCurrencies[int(currency)-1]
            args = [option,currency,amount]
        elif option == "7": # Previous Page
            args = [option]
        elif option == "8": # Next Page
            args = [option]
        elif option == "9": # Login
            ClientGUI.askUserName()
            username = input("-> ")
            ClientGUI.askPassword()
            password = input("-> ")
            args = [option,username,password]
        elif option == "0": # Quit
            args = [option]

        else:
            raise IOError

        return separator.join(args)



    
    def run(self):
        self.menu()
        self.closeConnection()

    def closeConnection(self):
        self.sock.close()
