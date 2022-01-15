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
        self.opcoes.append('SsAaRrOoCcDdIiVvLlPpMm') #logged in
        self.opcoes.append('SsFfAaEeRrCcIiVvPpMm') #not logged

<<<<<<< HEAD
    def login(self,option):
        username = self.client_gui.ask_info(self.clientInfo.loggedIn, self.clientInfo.getEvents(), 0)
        password = self.client_gui.ask_info(self.clientInfo.loggedIn, self.clientInfo.getEvents(), 1)
        
        #print(f"O username é {username} e a password é {password}")

        args = [option,username,password]
        response = self.requestServer(args)
        if response["LoggedIn"]:
            self.clientInfo.loggedIn = True
            self.client_gui.username = username
        else:
            self.client_gui.invalid_info(2)
        # print(response['Message'])
=======
>>>>>>> main
    
    def menu(self):
        inp = ''
        while inp != 'S':
            #ClientGUI.showEvents(self.clientInfo.getEvents())
            inp = "Q"
<<<<<<< HEAD

            if self.clientInfo.loggedIn:
                while inp not in self.opcoes[0]:
                    inp = self.client_gui.showMenu(self.clientInfo.loggedIn, self.clientInfo.wallet, self.clientInfo.getEvents())
            else:
                while inp not in self.opcoes[1]:
                    inp = self.client_gui.showMenu(self.clientInfo.loggedIn, self.clientInfo.wallet, self.clientInfo.getEvents())    
=======
            print(self.clientInfo.getNotifications(2))
            while inp not in 'SsFfAaEeRrOoCcDdIiCcMmVvAaPpHhNnLl':
                inp = self.client_gui.showMenu(self.clientInfo.loggedIn, self.clientInfo.wallet, self.clientInfo.getEvents())
            
>>>>>>> main
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
        #print(f"A opcao é {option}")
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
        eventID = self.client_gui.ask_info(self.clientInfo.loggedIn, self.clientInfo.getEvents(), 4)
        
        args = [option,"GET",eventID]
        response = self.requestServer(args)

        #TODO: reagir diferente dependendo da resposta
        print(response["Message"])
        if not response["Success"]:
            return

        aposta = -1

        while int(aposta) < 0 or int(aposta) > len(response["Event"]["Intervenors"])-1:
            aposta = self.client_gui.showDetailedEvent(self.clientInfo.loggedIn, self.clientInfo.getEvents(), response["Event"])
     
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
        args = ["M"]
        response = self.requestServer(args)

        aposta = self.client_gui.show_betslip(response, 6)
        args = [option,aposta]
        response = self.requestServer(args)

        print(response)

    def cancelBetSlip(self,option):
        args = [option]
        response = self.requestServer(args)

        print(response["Message"])

    def showBetSlip(self,option):
        args = [option]
        response = self.requestServer(args)

        self.client_gui.show_betslip(response, 5)
        print(response["BetSlip"])

    def concludeBetSlip(self,option): # TODO
        currency = ""
        amount = ""

        args = ["M"]
        response = self.requestServer(args)
        
        if self.client_gui.conclude_betslip(self.clientInfo.loggedIn, response) == 'S':
            while not currency.isdigit() or int(currency) < 0 or int(currency) >= len(self.clientInfo.availableCurrencies):
                currency = self.client_gui.pede_moeda(response, self.clientInfo.availableCurrencies, True)
            
            while not amount.isdigit() or int(amount) <= 0:    
                amount = self.client_gui.ask_amount(response)

            args = [option,amount,self.clientInfo.availableCurrencies[int(currency)]]
            message = self.requestServer(args)
            
            print(message)

    def depositMoney(self,option):
        currency = ""
        amount = ""

        while not currency.isdigit() or int(currency) < 0 or int(currency) >= len(self.clientInfo.availableCurrencies):
            currency = self.client_gui.pede_moeda(self.clientInfo.getEvents(), self.clientInfo.availableCurrencies, False)

        while not amount.isdigit() or int(amount) <= 0:    
            amount = self.client_gui.ask_info(self.clientInfo.loggedIn, self.clientInfo.getEvents(), 3)
        
        args = [option,self.clientInfo.availableCurrencies[int(currency)],amount]
        response = self.requestServer(args)

        print(response["Message"])


    def withdrawMoney(self,option):
        currency = ""
        amount = ""

<<<<<<< HEAD
        while not currency.isdigit() or currency < 0 or currency >= len(self.clientInfo.availableCurrencies):
            currency = self.client_gui.pede_moeda(self.clientInfo.getEvents(), self.clientInfo.availableCurrencies, False)
        
        while not amount.isdigit() or int(amount) <= 0:    
            amount = self.client_gui.ask_info(self.clientInfo.loggedIn, self.clientInfo.getEvents(), 3)
        
        args = [option,self.clientInfo.availableCurrencies[int(currency)],amount]
        mensagem = self.requestServer(args)
        print(mensagem["Message"])
=======
        args = [option,self.clientInfo.availableCurrencies[int(currency)],amount]
        self.requestServer(args)
>>>>>>> main

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

        args = [option,username,password]
        response = self.requestServer(args)
        if response["LoggedIn"]:
            self.clientInfo.loggedIn = True
            self.client_gui.username = username
        else:
            self.client_gui.invalid_info(0)
        # print(response['Message'])

    def logout(self,option):
        args = [option]
        self.requestServer(args)
        self.clientInfo.loggedIn = False
        self.client_gui.username = None
        
    def register(self,option):
        username = self.client_gui.ask_info(self.clientInfo.loggedIn, self.clientInfo.getEvents(), 0)
        password = self.client_gui.ask_info(self.clientInfo.loggedIn, self.clientInfo.getEvents(), 1)
        birthdate = self.client_gui.ask_info(self.clientInfo.loggedIn, self.clientInfo.getEvents(), 2)
        
        args = [option,username,password,birthdate]
        response = self.requestServer(args)

        print(response['Success'])
    
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
