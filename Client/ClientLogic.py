import socket
import ClientGUI
import ClientInfo
import json

class ClientLogic:
    
    sock : socket.socket
    availableCurrencies : list
    clientInfo : ClientInfo.ClientInfo

    def __init__(self,sock,currencies):
        self.sock = sock
        self.availableCurrencies = currencies
        self.clientInfo = ClientInfo.ClientInfo()

    def menu(self):
        inp = ''
        while inp != '0':
            ClientGUI.showMenu(self.clientInfo.loggedIn)
            inp = input(" -> ")
            option = int(inp)
            self.handleInput(option)

    def requestServer(self,message):
        data = message.encode('utf-8')
        self.sock.send(data)
        data = self.sock.recv(256)
        response = json.loads(data.decode('utf-8'))
        return response



    def handleInput(self,option):
        args = []
        option = str(option)

        if option == "1": # Add Bet To Bet Slip
            self.addBetToBetSlip(option)
        elif option == "2": # Remove Bet From Bet Slip
            self.removeBetFromBetSlip(option)
        elif option == "3": # Cancel Bet Slip
            args = [option]
        elif option == "4": # Show Bet Slip
            args = [option]
        elif option == "5": # Conclude Bet Slip
            message = self.handleInput(4)
            data = message.encode('utf-8')
            self.sock.send(data)
            data = self.sock.recv(256)
            print(data.decode("utf-8"))
            ClientGUI.askAmount()
            amount = input("-> ")
            currency = ''
            ClientGUI.askCurrency(self.availableCurrencies)
            currency = input("-> ")
            currency = self.availableCurrencies[int(currency)-1]
            args = [option,amount,currency]
        elif option == "6": # Deposit Money
            ClientGUI.askAmount()
            amount = input("-> ")
            currency = ''
            ClientGUI.askCurrency(self.availableCurrencies)
            currency = input("-> ")
            currency = self.availableCurrencies[int(currency)-1]
            args = [option,currency,amount]
        elif option == "7": # Withdraw Money
            ClientGUI.askAmount()
            amount = input("-> ")
            currency = ''
            ClientGUI.askCurrency(self.availableCurrencies)
            currency = input("-> ")
            currency = self.availableCurrencies[int(currency)-1]
            args = [option,currency,amount]
        elif option == "8": # Previous Page
            args = [option]
        elif option == "9": # Next Page
            args = [option]
        elif option == "10": # Login/Logout
            ClientGUI.askUserName()
            username = input("-> ")
            ClientGUI.askPassword()
            password = input("-> ")
            args = [option,username,password]
        elif option == "11": # Register
            self.registerUser(option)
        elif option == "0": # Quit
            args = [option]
            message = " ".join(args)
            self.requestServer(message)

        else:
            raise IOError

    def addBetToBetSlip(self,option):
        ClientGUI.askEvent()
        eventID = input("-> ")

        ClientGUI.showDetailedEvent()
        result = input("-> ")

        args = [option,eventID,result]
        message = " ".join(args)
        self.requestServer(message)

    def removeBetFromBetSlip(self,option):
        ClientGUI.askEvent()
        eventID = input("-> ")
        args = [option,eventID]
        message = " ".join(args)
        self.requestServer(message)

    def registerUser(self,option):
        ClientGUI.askUserName()
        username = input("-> ")

        ClientGUI.askPassword()
        password = input("-> ")

        ClientGUI.askBirthDate()
        birthdate = input("-> ")

        args = [option,username,password,birthdate]
        message = " ".join(args)
        response = self.requestServer(message)

        print(response)


    def run(self):
        self.menu()
        self.closeConnection()

    def closeConnection(self):
        self.sock.close()
