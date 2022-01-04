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

    def login(self,option):
        username = self.client_gui.ask_info(self.clientInfo.events, 0)
        password = self.client_gui.ask_info(self.clientInfo.events, 1)
        
        #print(f"O username é {username} e a password é {password}")

        args = [option,username,password]
        response = self.requestServer(args)
        if response["LoggedIn"]:
            self.clientInfo.loggedIn = True
            self.client_gui.username = username
        else:
            self.client_gui.invalid_info(0)
        # print(response['Message'])
    
    def menu(self):
        inp = ''
        while inp != 'S':
            #ClientGUI.showEvents(self.clientInfo.events)
            
            inp = "Q"

            while inp not in 'SsFfAaEeRrOoCcDdIi':
                inp = self.client_gui.showMenu(self.clientInfo.loggedIn, self.clientInfo.wallet, self.clientInfo.events)
            
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
            self.clientInfo.updateInfo(response["Wallet"],response["Events"],response["Currencies"])
            self.client_gui.wallet = self.clientInfo.wallet

        return response

   

    def handle_input(self,option): # TODO: Exchange currencies
        actions = {
            "I":self.addBetToBetSlip,
            "R":self.removeBetFromBetSlip,
            "3":self.cancelBetSlip,
            "4":self.showBetSlip,
            "5":self.concludeBetSlip,
            "D":self.depositMoney,
            "L":self.withdrawMoney,
            "8":self.changePage, # Previous Page
            "9":self.changePage, # Next Page
            "F":self.login,
            "E":self.register,
            "S":self.quit,
            "O":self.logout
            #show history
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
        if not response["Found"]:
            return

        self.client_gui.showDetailedEvent(response["Event"])
        result = input("-> ")

        args = [option,"PUT",eventID,result]
        response = self.requestServer(args)

        print(response["Message"])

    def removeBetFromBetSlip(self,option):
        # Should we show betslip before deciding to remove bet?
        self.client_gui.askEvent()
        eventID = input("-> ")
        args = [option,eventID]
        response = self.requestServer(args)

        print(response["Message"])

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
        currency = self.client_gui.pede_moeda(self.clientInfo.events, self.clientInfo.availableCurrencies)
        amount = self.client_gui.ask_info(self.clientInfo.events, 3)
        
        
        print(f"O amount é {amount} e a currency é {currency}")

        args = [option,self.clientInfo.availableCurrencies[int(currency)],amount]
        self.requestServer(args)
        # Update clientInfo

    def withdrawMoney(self,option):
        currency = self.client_gui.pede_moeda(self.clientInfo.events, self.clientInfo.availableCurrencies)
        amount = self.client_gui.ask_info(self.clientInfo.events, 3)

        args = [option,currency,amount]
        self.requestServer(args)

    def changePage(self,option): # TODO
        args = [option]
        self.requestServer(args)

    def showBetHistory(self,option): # TODO
        args = [option]
        self.requestServer(args)
    
        
    def logout(self,option):
        args = [option]
        self.requestServer(args)
        self.clientInfo.loggedIn = False
        self.client_gui.username = None
        
    def register(self,option):
        username = self.client_gui.ask_info(self.clientInfo.events, 0)
        password = self.client_gui.ask_info(self.clientInfo.events, 1)
        birthdate = self.client_gui.ask_info(self.clientInfo.events, 2)
        
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
