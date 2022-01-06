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
    opcoes : list

    def __init__(self,sock,info):
        self.sock = sock
        self.clientInfo = ClientInfo.ClientInfo(info)
        self.client_gui = ClientGUI()
        self.opcoes = list()
        self.opcoes.append('SsAaRrOoCcDdIiVvLl') #logged in
        self.opcoes.append('SsFfAaEeRrCcIiVv') #not logged

    def login(self,option):
        username = self.client_gui.ask_info(self.clientInfo.loggedIn, self.clientInfo.events, 0)
        password = self.client_gui.ask_info(self.clientInfo.loggedIn, self.clientInfo.events, 1)
        
        #print(f"O username é {username} e a password é {password}")

        args = [option,username,password]
        response = self.requestServer(args)
        if response["LoggedIn"]:
            self.clientInfo.loggedIn = True
            self.client_gui.username = username
        else:
            self.client_gui.invalid_info(2)
        # print(response['Message'])
    
    def menu(self):
        inp = ''
        while inp != 'S':
            #ClientGUI.showEvents(self.clientInfo.events)
            
            inp = "Q"

            if self.clientInfo.loggedIn:
                while inp not in self.opcoes[0]:
                    inp = self.client_gui.showMenu(self.clientInfo.loggedIn, self.clientInfo.wallet, self.clientInfo.events)
            else:
                while inp not in self.opcoes[1]:
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
        #print(f"A opcao é {option}")
        actions = {
            "I":self.addBetToBetSlip,
            "R":self.removeBetFromBetSlip,
            "3":self.cancelBetSlip,
            "4":self.showBetSlip,
            "V":self.concludeBetSlip,
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
        eventID = self.client_gui.ask_info(self.clientInfo.loggedIn, self.clientInfo.events, 4)
        
        args = [option,"GET",eventID]
        response = self.requestServer(args)

        #TODO: reagir diferente dependendo da resposta
        print(response["Message"])

        if not response["Found"]:
            return

        aposta = -1

        while int(aposta) < 0 or int(aposta) > len(response["Event"]["Intervenors"])-1:
            aposta = self.client_gui.showDetailedEvent(self.clientInfo.loggedIn, self.clientInfo.events, response["Event"])
     
        if response["Event"]["Sport"]["Type"] == "WinDraw":
            if int(aposta) == 2:
                aposta = "1"
            elif int(aposta) == 1:
                aposta = "2"
        print(f"Adding aposta {aposta}")
        args = [option,"PUT",eventID,aposta]
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
        self.client_gui.conclude_betslip(self.clientInfo.loggedIn, self.clientInfo.events) #mudar para o betslip do gajo
        
        self.client_gui.pede_moeda(self.clientInfo)
        """
        ClientGUI.askAmount()
        amount = input("-> ")
        currency = ''
        ClientGUI.askCurrency(self.clientInfo.availableCurrencies)
        currency = input("-> ")
        currency = self.clientInfo.availableCurrencies[int(currency)-1]
        args = [option,amount,currency]
        self.requestServer(args)
        """
    def depositMoney(self,option):
        currency = ""
        amount = ""

        while not currency.isdigit() or int(currency) <= 0 or int(currency) >= len(self.clientInfo.availableCurrencies):
            currency = self.client_gui.pede_moeda(self.clientInfo.events, self.clientInfo.availableCurrencies)

        while not amount.isdigit() or int(amount) <= 0:    
            amount = self.client_gui.ask_info(self.clientInfo.loggedIn, self.clientInfo.events, 3)
        
        args = [option,self.clientInfo.availableCurrencies[int(currency)],amount]
        self.requestServer(args)
        # Update clientInfo

    def withdrawMoney(self,option):
        currency = -1
        amount = -1

        while not currency.isdigit() or currency <= 0 or currency >= len(self.clientInfo.availableCurrencies):
            currency = self.client_gui.pede_moeda(self.clientInfo.events, self.clientInfo.availableCurrencies)
        
        while not amount.isdigit() or int(amount) <= 0:    
            amount = self.client_gui.ask_info(self.clientInfo.loggedIn, self.clientInfo.events, 3)
        
        args = [option,self.clientInfo.availableCurrencies[int(currency)],amount]
        mensagem = self.requestServer(args)
        print(mensagem["Message"])

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
        username = self.client_gui.ask_info(self.clientInfo.loggedIn, self.clientInfo.events, 0)
        password = self.client_gui.ask_info(self.clientInfo.loggedIn, self.clientInfo.events, 1)
        birthdate = self.client_gui.ask_info(self.clientInfo.loggedIn, self.clientInfo.events, 2)
        
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
