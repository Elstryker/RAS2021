import socket
import ClientGUI
import ClientInfo
import json

class ClientLogic:
    
    sock : socket.socket
    clientInfo : ClientInfo.ClientInfo

    def __init__(self,sock,currencies):
        self.sock = sock
        self.clientInfo = ClientInfo.ClientInfo(currencies)

    def menu(self):
        inp = ''
        while inp != '0':
            ClientGUI.showMenu(self.clientInfo.loggedIn)
            inp = input(" -> ")
            option = int(inp)
            if self.clientInfo.loggedIn:
                self.handleInputLoggedIn(option)
            else:
                self.handleInputNotLoggedIn(option)

    def requestServer(self,message):
        data = message.encode('utf-8')
        self.sock.send(data)
        data = self.sock.recv(256)
        response = json.loads(data.decode('utf-8'))
        return response

    def handleInputNotLoggedIn(self,option):
        option = str(option)

        if option == "1": # Add Bet To Bet Slip
            self.addBetToBetSlip(option)
        elif option == "2": # Remove Bet From Bet Slip
            self.removeBetFromBetSlip(option)
        elif option == "3": # Cancel Bat Slip
            self.cancelBetSlip(option)
        elif option == "4": # Show Bet Slip
            self.showBetSlip(option)
        elif option == "5": # Previus Page
            self.changePage(option)
        elif option == "6": # Next Page
            self.changePage(option)
        elif option == "7": # Login
            self.login(option)
        elif option == "8": # Register
            self.register(option)
        elif option == "0": # Quit
            self.quit(option)
        else:
            raise IOError

    def handleInputLoggedIn(self,option): # TODO: Exchange currencies
        option = str(option)

        if option == "1": # Add Bet To Bet Slip
            self.addBetToBetSlip(option)
        elif option == "2": # Remove Bet From Bet Slip
            self.removeBetFromBetSlip(option)
        elif option == "3": # Cancel Bet Slip
            self.cancelBetSlip(option)
        elif option == "4": # Show Bet Slip
            self.showBetSlip(option)
        elif option == "5": # Conclude Bet Slip
            self.concludeBetSlip(option)
        elif option == "6": # Deposit Money
            self.depositMoney(option)
        elif option == "7": # Withdraw Money
            self.withdrawMoney(option)
        elif option == "8": # Previous Page
            self.changePage(option)
        elif option == "9": # Next Page
            self.changePage(option)
        elif option == "10": # See Bet History
            self.showBetHistory(option)
        elif option == "11": # Logout
            self.register(option)
        elif option == "0": # Quit
            self.quit(option)
        else:
            raise IOError

    def addBetToBetSlip(self,option): # TODO
        ClientGUI.askEvent()
        eventID = input("-> ")

        ClientGUI.showDetailedEvent()
        result = input("-> ")

        args = [option,eventID,result]
        message = ";".join(args)
        self.requestServer(message)

    def removeBetFromBetSlip(self,option): # TODO
        ClientGUI.askEvent()
        eventID = input("-> ")
        args = [option,eventID]
        message = ";".join(args)
        self.requestServer(message)

    def cancelBetSlip(self,option): # TODO
        args = [option]
        message = ";".join(args)
        self.requestServer(message)

    def showBetSlip(self,option): # TODO
        args = [option]
        message = ";".join(args)
        self.requestServer(message)

    def concludeBetSlip(self,option): # TODO
        message = self.handleInput(4)
        data = message.encode('utf-8')
        self.sock.send(data)
        data = self.sock.recv(256)
        print(data.decode("utf-8"))
        ClientGUI.askAmount()
        amount = input("-> ")
        currency = ''
        ClientGUI.askCurrency(self.clientInfo.availableCurrencies)
        currency = input("-> ")
        currency = self.clientInfo.availableCurrencies[int(currency)-1]
        args = [option,amount,currency]
        message = ";".join(args)
        self.requestServer(message)

    def depositMoney(self,option): # TODO
        ClientGUI.askAmount()
        amount = input("-> ")
        currency = ''
        ClientGUI.askCurrency(self.clientInfo.availableCurrencies)
        currency = input("-> ")
        currency = self.clientInfo.availableCurrencies[int(currency)-1]
        args = [option,currency,amount]
        message = ";".join(args)
        self.requestServer(message)
        # Update clientInfo

    def withdrawMoney(self,option): # TODO
        ClientGUI.askAmount()
        amount = input("-> ")
        currency = ''
        ClientGUI.askCurrency(self.clientInfo.availableCurrencies)
        currency = input("-> ")
        currency = self.clientInfo.availableCurrencies[int(currency)-1]
        args = [option,currency,amount]
        message = ";".join(args)
        self.requestServer(message)

    def changePage(self,option): # TODO
        args = [option]
        message = ";".join(args)
        self.requestServer(message)

    def showBetHistory(self,option): # TODO
        args = [option]
        message = ";".join(args)
        self.requestServer(message)
    
    def login(self,option):
        ClientGUI.askUserName()
        username = input("-> ")
        ClientGUI.askPassword()
        password = input("-> ")
        args = [option,username,password]
        message = ";".join(args)
        response = self.requestServer(message)
        if response["LoggedIn"]:
            self.clientInfo.loggedIn = True
        print(response['Message'])
        
    def logout(self,option):
        args = [option]
        message = ";".join(args)
        response = self.requestServer(message)
        self.clientInfo.loggedIn = False
        print(response['Message'])

    def register(self,option):
        ClientGUI.askUserName()
        username = input("-> ")

        ClientGUI.askPassword()
        password = input("-> ")

        ClientGUI.askBirthDate()
        birthdate = input("-> ")

        args = [option,username,password,birthdate]
        message = ";".join(args)
        response = self.requestServer(message)

        print(response['Message'])
    
    def quit(self,option):
        args = [option]
        message = ";".join(args)
        reply = self.requestServer(message)
        print(reply['Message'])

    def run(self):
        self.menu()
        self.closeConnection()

    def closeConnection(self):
        self.sock.close()
