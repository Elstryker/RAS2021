import socket
from ClientGUI import ClientGUI
import ClientInfo
import json
from rich.console import Console
from rich import box
from rich.prompt import Prompt

class ClientLogic:
    
    sock : socket.socket
    clientInfo : ClientInfo.ClientInfo
    client_gui : ClientGUI
    inputs_logged : str
    inputs_notlogged : str

    def __init__(self,sock,info):
        self.sock = sock
        self.clientInfo = ClientInfo.ClientInfo(info)
        self.client_gui = ClientGUI()

    
    def menu(self):
        inp = ''
        while inp != 'S':
            #ClientGUI.showEvents(self.clientInfo.getEvents())
            inp = "Q"
            print(self.clientInfo.getNotifications(2))
            while inp not in 'SsFfAaEeRrOoCcDdIiCcMmVvAaPpHhNnLl':
                inp = self.client_gui.showMenu(self.clientInfo.loggedIn, self.clientInfo.wallet, self.clientInfo.getEvents())
            
            inp = inp.upper()
            
            self.handle_input(inp)
            
    def requestServer(self,args):
        message = ";".join(args)

        data = message.encode('utf-8')
        self.sock.send(data)
        data = self.sock.recv(2048)
        response = json.loads(data.decode('utf-8'))

        # Retrieve additional info
        if args[0] != "S": # See if it just wants to quit
            self.clientInfo.updateInfo(response)
            self.client_gui.wallet = self.clientInfo.wallet

        return response

   

    def handle_input(self,option): # TODO: Exchange currencies
        actions = {
            "I":self.addBetToBetSlip,
            "R":self.removeBetFromBetSlip,
            "C":self.cancelBetSlip,
            "M":self.showBetSlip,
            "V":self.concludeBetSlip,
            "D":self.depositMoney,
            "L":self.withdrawMoney,
            "A":self.changePage, # Previous Page
            "P":self.changePage, # Next Page
            "H":self.showBetHistory,
            "N":self.exchangeCurrency,
            "F":self.login,
            "E":self.register,
            "S":self.quit,
            "O":self.logout
        }
        toDo = actions.get(option,self.noSuchAction)
        toDo(option)

    def noSuchAction(self,option):
        print("Opção errada:",option)

    def addBetToBetSlip(self,option):
        self.client_gui.askEvent()
        eventID = input("-> ")

        args = [option,"GET",eventID]
        response = self.requestServer(args)

        print(response["Message"])
        if not response["Success"]:
            return

        self.client_gui.showDetailedEvent(response["Event"])
        result = input("-> ")
        if len(response["Event"]["Intervenors"]) <= int(result) and int(result) >= 0:
            print("No good input")
            return

        if not self.clientInfo.loggedIn:
            self.clientInfo.addBetNotLoggedIn(eventID,result)
            args = ["P"]
            self.requestServer(args)

            return

        args = [option,"PUT",eventID,result]
        response = self.requestServer(args)

        print(response["Message"])

    def removeBetFromBetSlip(self,option):
        self.client_gui.askEvent()
        eventID = input("-> ")

        if not self.clientInfo.loggedIn:
            args = ["P"]
            self.requestServer(args)
            self.clientInfo.removeBetNotLoggedIn(eventID)

            return

        args = [option,eventID]
        response = self.requestServer(args)

        print(response["Message"])

    def cancelBetSlip(self,option):
        args = [option]
        response = self.requestServer(args)

        if not self.clientInfo.loggedIn:
            args = ["P"]
            self.requestServer(args)
            self.clientInfo.cancelBetSlipNotLoggedIn()

            return

        print(response["Message"])

    def showBetSlip(self,option):
        if not self.clientInfo.loggedIn:
            args = ["P"]
            self.requestServer(args)
            betSlip = self.clientInfo.getBetSlipNotLoggedIn()
            print(betSlip)

            return

        args = [option]
        response = self.requestServer(args)

        print(response["Message"])
        print(response["BetSlip"])

    def concludeBetSlip(self,option): # TODO
        self.showBetSlip("M")
        # Não consegui testar por causa dos prints :/
        #ClientGUI.askAmount()
        amount = input("-> ")

        currency = ''
        #ClientGUI.askCurrency(self.clientInfo.availableCurrencies)
        currency = input("-> ")
        currency = self.clientInfo.availableCurrencies[int(currency)-1]

        args = [option,amount,currency]
        response = self.requestServer(args)

        print(response["Message"])

    def depositMoney(self,option):
        currency = self.client_gui.pede_moeda(self.clientInfo.getEvents(), self.clientInfo.availableCurrencies)
        amount = self.client_gui.ask_info(self.clientInfo.getEvents(), 3)
        
        
        print(f"O amount é {amount} e a currency é {currency}")

        args = [option,self.clientInfo.availableCurrencies[int(currency)],amount]
        response = self.requestServer(args)

        print(response["Message"])


    def withdrawMoney(self,option):
        currency = self.client_gui.pede_moeda(self.clientInfo.getEvents(), self.clientInfo.availableCurrencies)
        amount = self.client_gui.ask_info(self.clientInfo.getEvents(), 3)

        args = [option,self.clientInfo.availableCurrencies[int(currency)],amount]
        self.requestServer(args)

    def changePage(self,option):
        self.clientInfo.previousPage() if option == "A" else self.clientInfo.nextPage()

        args = [option]
        self.requestServer(args)


    def showBetHistory(self,option):
        args = [option]
        response = self.requestServer(args)

        print(response["Message"])
        print(response["History"])

        # Falta GUI e decisões

    def exchangeCurrency(self,option):
        fromCurrency = self.client_gui.pede_moeda(self.clientInfo.getEvents(), self.clientInfo.availableCurrencies)
        toCurrency = self.client_gui.pede_moeda(self.clientInfo.getEvents(), self.clientInfo.availableCurrencies)

        amount = self.client_gui.ask_info(self.clientInfo.getEvents(), 3)

        args = [option,self.clientInfo.availableCurrencies[int(fromCurrency)],self.clientInfo.availableCurrencies[int(toCurrency)],amount]
        response = self.requestServer(args)

        print(response["Message"])
    
    
    def login(self,option):
        username = self.client_gui.ask_info(self.clientInfo.getEvents(), 0)
        password = self.client_gui.ask_info(self.clientInfo.getEvents(), 1)
        
        #print(f"O username é {username} e a password é {password}")

        args = [option,username,password,self.clientInfo.getBetSlipNotLoggedInToSend()]
        response = self.requestServer(args)
        if response["LoggedIn"]:
            self.clientInfo.loggedIn = True
            self.client_gui.username = username
            self.clientInfo.cancelBetSlipNotLoggedIn()
        else:
            self.client_gui.invalid_info(0)
        # print(response['Message'])

    def logout(self,option):
        args = [option]
        self.requestServer(args)
        self.clientInfo.loggedIn = False
        self.client_gui.username = None
        
    def register(self,option):
        username = self.client_gui.ask_info(self.clientInfo.getEvents(), 0)
        password = self.client_gui.ask_info(self.clientInfo.getEvents(), 1)
        birthdate = self.client_gui.ask_info(self.clientInfo.getEvents(), 2)
        
        args = [option,username,password,birthdate]
        response = self.requestServer(args)

        print(response['Message'])
    
    def quit(self,option):
        self.client_gui.goodbye()
        
        args = [option]
        reply = self.requestServer(args)
        
        print(reply['Message'])

    def run(self):
        self.menu()
        self.closeConnection()

    def closeConnection(self):
        self.sock.close()
