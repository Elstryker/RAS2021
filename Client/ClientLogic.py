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

    def requestServer(self,args):
        message = ";".join(args)

        data = message.encode('utf-8')
        self.sock.send(data)
        data = self.sock.recv(256)
        response = json.loads(data.decode('utf-8'))

        # Retrieve additional info
        if args[0] != "0": # See if it just wants to quit
            self.clientInfo.updateInfo(response["Wallet"],response["Events"],response["DetailedEvent"],response["Currencies"])
            print(self.clientInfo.wallet)

        return response

    def handleInputNotLoggedIn(self,option):
        option = str(option)
        actions = {
            "1":self.addBetToBetSlip,
            "2":self.removeBetFromBetSlip,
            "3":self.cancelBetSlip,
            "4":self.showBetSlip,
            "5":self.changePage,
            "6":self.changePage,
            "7":self.login,
            "8":self.register,
            "0":self.quit
        }

        toDo = actions.get(option,self.noSuchAction)
        toDo(option)

    def handleInputLoggedIn(self,option): # TODO: Exchange currencies
        option = str(option)
        actions = {
            "1":self.addBetToBetSlip,
            "2":self.removeBetFromBetSlip,
            "3":self.cancelBetSlip,
            "4":self.showBetSlip,
            "5":self.concludeBetSlip,
            "6":self.depositMoney,
            "7":self.withdrawMoney,
            "8":self.changePage, # Previous Page
            "9":self.changePage, # Next Page
            "10":self.login,
            "11":self.register,
            "0":self.quit
        }
        toDo = actions.get(option,self.noSuchAction)
        toDo(option)

    def noSuchAction(self,option):
        raise IOError

    def addBetToBetSlip(self,option): # TODO
        ClientGUI.askEvent()
        eventID = input("-> ")

        ClientGUI.showDetailedEvent()
        result = input("-> ")

        args = [option,eventID,result]
        self.requestServer(args)

    def removeBetFromBetSlip(self,option): # TODO
        ClientGUI.askEvent()
        eventID = input("-> ")
        args = [option,eventID]
        self.requestServer(args)

    def cancelBetSlip(self,option): # TODO
        args = [option]
        self.requestServer(args)

    def showBetSlip(self,option): # TODO
        args = [option]
        self.requestServer(args)

    def concludeBetSlip(self,option): # TODO
        args = self.handleInput(4)
        data = args.encode('utf-8')
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
        self.requestServer(args)

    def depositMoney(self,option):
        ClientGUI.askAmount()
        amount = input("-> ")

        currency = ''
        ClientGUI.askCurrency(self.clientInfo.availableCurrencies)
        currency = input("-> ")

        currency = self.clientInfo.availableCurrencies[int(currency)-1]
        args = [option,currency,amount]
        self.requestServer(args)
        # Update clientInfo

    def withdrawMoney(self,option):
        ClientGUI.askAmount()
        amount = input("-> ")

        currency = ''
        ClientGUI.askCurrency(self.clientInfo.availableCurrencies)
        currency = input("-> ")
        currency = self.clientInfo.availableCurrencies[int(currency)-1]

        args = [option,currency,amount]
        self.requestServer(args)

    def changePage(self,option): # TODO
        args = [option]
        self.requestServer(args)

    def showBetHistory(self,option): # TODO
        args = [option]
        self.requestServer(args)
    
    def login(self,option):
        ClientGUI.askUserName()
        username = input("-> ")

        ClientGUI.askPassword()
        password = input("-> ")
        
        args = [option,username,password]
        response = self.requestServer(args)
        if response["LoggedIn"]:
            self.clientInfo.loggedIn = True
        print(response['Message'])
        
    def logout(self,option):
        args = [option]
        response = self.requestServer(args)
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
        response = self.requestServer(args)

        print(response['Message'])
    
    def quit(self,option):
        args = [option]
        reply = self.requestServer(args)
        print(reply['Message'])

    def run(self):
        self.menu()
        self.closeConnection()

    def closeConnection(self):
        self.sock.close()
