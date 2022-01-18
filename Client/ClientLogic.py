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
            inp = "Q"
            notifs = self.clientInfo.getNotifications(2)
            
            while inp not in 'SsFfAaEeRrOoCcDdIiCcMmVvAaPpHhNnLlTt':
                inp = self.client_gui.showMenu(self.clientInfo.loggedIn, self.clientInfo.wallet, self.clientInfo.getEvents(), self.clientInfo.getPages(), notifs)
            
            inp = inp.upper()
            
            self.handle_input(inp)
            
    def requestServer(self,args):
        message = ";".join(args)

        data = message.encode('utf-8')
        self.sock.send(data)
        data = self.sock.recv(2048)
        response = json.loads(data.decode('utf-8'))

        # Retrieve additional info
        if args[0] != "S": 
            self.clientInfo.updateInfo(response)
            self.client_gui.wallet = self.clientInfo.wallet

        return response


    def filter(self,option):
        resposta = "F"

        while not resposta.isdigit() or int(resposta) < 0 or int(resposta) >= len(self.clientInfo.filtros):
            resposta = self.client_gui.pergunta_filtros(self.clientInfo.loggedIn, self.clientInfo.getFiltros(), self.clientInfo.getFiltros_ativos(), self.clientInfo.availableCurrencies, self.clientInfo.getEvents(), self.clientInfo.getPages())
        
        #print(f"opcao: {self.clientInfo.filtros[int(resposta)]}")
        escolha = self.clientInfo.filtros[int(resposta)]
        
        if escolha in self.clientInfo.filtros_ativos:
            self.clientInfo.filtros_ativos.remove(escolha)
        else:
            self.clientInfo.filtros_ativos.append(escolha)



    def handle_input(self,option):
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
            "T":self.filter,
            "S":self.quit,
            "O":self.logout
        }
        toDo = actions.get(option,self.noSuchAction)
        toDo(option)

    def noSuchAction(self,option):
        print("Opção errada:",option)

    def addBetToBetSlip(self,option):
        eventID = self.client_gui.ask_info(self.clientInfo.loggedIn, self.clientInfo.getEvents(), 4, self.clientInfo.getPages())
        
        args = [option,"GET",eventID]
        response = self.requestServer(args)

        #TODO: reagir diferente dependendo da resposta
        print(response["Message"])
        if not response["Success"]:
            return

        aposta = -1

        while int(aposta) < 0 or int(aposta) > len(response["Event"]["Intervenors"])-1:
            aposta = self.client_gui.showDetailedEvent(self.clientInfo.loggedIn, self.clientInfo.getEvents(), response["Event"], self.clientInfo.getPages())


        if response["Event"]["Sport"]["Type"] == "WinDraw":
            if int(aposta) == 2:
                aposta = "1"
            elif int(aposta) == 1:
                aposta = "2"
        
        if not self.clientInfo.loggedIn:
            self.clientInfo.addBetNotLoggedIn(eventID,result)
            args = ["P"]
            self.requestServer(args)

            return
        print(f"Adding aposta {aposta}")
        args = [option,"PUT",eventID,aposta]
        response = self.requestServer(args)

        print(response["Message"])

    def removeBetFromBetSlip(self,option):
        if not self.clientInfo.loggedIn:
            eventos = self.clientInfo.getBetSlip()
            self.client_gui.show_betslip(eventos, 6)

            args = ["P"]
            self.requestServer(args)
            self.clientInfo.removeBetNotLoggedIn(eventID)
            return

        args = ["M"]
        response = self.requestServer(args)
        aposta = self.client_gui.show_betslip(response, 6)


           

            

        args = [option,aposta]
        response = self.requestServer(args)

        print(response)

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

        self.client_gui.show_betslip(self.clientInfo.loggedIn, response, 5)
        print(response["BetSlip"])

    def concludeBetSlip(self,option): # TODO
        currency = ""
        amount = ""


        if self.clientInfo.loggedIn:
            args = ["M"]
            response = self.requestServer(args)
            
            if self.client_gui.conclude_betslip(self.clientInfo.loggedIn, response) == 'S':
                while not currency.isdigit() or int(currency) < 1 or int(currency) >= len(self.clientInfo.availableCurrencies):
                    currency = self.client_gui.pede_moeda(self.clientInfo.loggedIn, response, self.clientInfo.availableCurrencies, True, self.clientInfo.getPages())
                
                while not amount.isdigit() or int(amount) <= 0:    
                    amount = self.client_gui.ask_amount(self.clientInfo.loggedIn, response)

                args = [option,amount,self.clientInfo.availableCurrencies[int(currency)]]
                message = self.requestServer(args)
                
                print(message)
        else:
            self.client_gui.invalid_info(self.clientInfo.loggedIn, 1)

    def depositMoney(self,option):
        currency = ""
        amount = ""

        while not currency.isdigit() or int(currency) < 1 or int(currency) > 100 or int(currency) >= len(self.clientInfo.availableCurrencies):
            currency = self.client_gui.pede_moeda(self.clientInfo.loggedIn, self.clientInfo.getEvents(), self.clientInfo.availableCurrencies,  False, self.clientInfo.getPages())

        while not amount.isdigit() or int(amount) <= 0:    
            amount = self.client_gui.ask_info(self.clientInfo.loggedIn, self.clientInfo.getEvents(), 3, self.clientInfo.getPages())
        
        args = [option,self.clientInfo.availableCurrencies[int(currency)],amount]
        response = self.requestServer(args)

        print(response["Message"])


    def withdrawMoney(self,option):
        currency = ""
        amount = ""

        while not currency.isdigit() or int(currency) < 1 or int(currency) >= len(self.clientInfo.availableCurrencies):
            currency = self.client_gui.pede_moeda(self.clientInfo.loggedIn, self.clientInfo.getEvents(), self.clientInfo.availableCurrencies, False, self.clientInfo.getPages())
        
        while not amount.isdigit() or int(amount) <= 0:    
            amount = self.client_gui.ask_info(self.clientInfo.loggedIn, self.clientInfo.getEvents(), 3, self.clientInfo.getPages())
        
        args = [option,self.clientInfo.availableCurrencies[int(currency)],amount]
        mensagem = self.requestServer(args)
        print(mensagem["Message"])

    def changePage(self,option):
        self.clientInfo.previousPage() if option == "A" else self.clientInfo.nextPage()

        args = [option]
        self.requestServer(args)
        


    def showBetHistory(self,option):
        args = [option]
        response = self.requestServer(args)
        
        if len(response["History"]) == 0:
            self.client_gui.invalid_info(self.clientInfo.loggedIn, 3)
        else:
            escolha = "a"

            while not escolha.isdigit() or int(escolha) < 0:
                escolha = self.client_gui.show_history(self.clientInfo.loggedIn, response["History"])

            boletim = self.encontra_boletim(response["History"], int(escolha))

            self.client_gui.show_betslip(self.clientInfo.loggedIn, {"BetSlip":boletim}, 5)

        # Falta GUI e decisões
    def filtrar (self, ):
        pass


    def encontra_boletim(self, boletins : list, escolha : int):
        resposta = None
        print(boletins)
        while resposta is None:
            for boletim in boletins:
                if boletim["Id"] == escolha:
                    resposta = boletim

        return resposta

    def exchangeCurrency(self,option):
        fromCurrency = self.client_gui.pede_moeda(self.clientInfo.loggedIn, self.clientInfo.getEvents(), self.clientInfo.availableCurrencies, False, self.clientInfo.getPages(), 1)
        toCurrency = self.client_gui.pede_moeda(self.clientInfo.loggedIn, self.clientInfo.getEvents(), self.clientInfo.availableCurrencies, False, self.clientInfo.getPages(), 2)

        amount = self.client_gui.ask_info(self.clientInfo.loggedIn, self.clientInfo.getEvents(), 3, self.clientInfo.getPages())

        args = [option,self.clientInfo.availableCurrencies[int(fromCurrency)],self.clientInfo.availableCurrencies[int(toCurrency)],amount]
        response = self.requestServer(args)

        print(response["Message"])
    
    
    def login(self,option):
        username = self.client_gui.ask_info(self.clientInfo.loggedIn, self.clientInfo.getEvents(), 0, self.clientInfo.getPages())
        password = self.client_gui.ask_info(self.clientInfo.loggedIn, self.clientInfo.getEvents(), 1, self.clientInfo.getPages())
        
        #print(f"O username é {username} e a password é {password}")

        args = [option,username,password,self.clientInfo.getBetSlipNotLoggedInToSend()]
        response = self.requestServer(args)
        if response["LoggedIn"]:
            self.clientInfo.loggedIn = True
            self.client_gui.username = username
            self.clientInfo.cancelBetSlipNotLoggedIn()
        else:
            self.client_gui.invalid_info(self.clientInfo.loggedIn, 2)
        # print(response['Message'])

    def logout(self,option):
        args = [option]
        self.requestServer(args)
        self.clientInfo.loggedIn = False
        self.client_gui.username = None
        
    def register(self,option):
        username = self.client_gui.ask_info(self.clientInfo.loggedIn, self.clientInfo.getEvents(), 0, self.clientInfo.getPages())
        password = ""
        password_confirmation = ""
        
        password = self.client_gui.ask_info(self.clientInfo.loggedIn, self.clientInfo.getEvents(), 1, self.clientInfo.getPages())
        password_confirmation = self.client_gui.ask_info(self.clientInfo.loggedIn, self.clientInfo.getEvents(), 8, self.clientInfo.getPages())
        
        if password == password_confirmation:        
            birthdate = self.client_gui.ask_info(self.clientInfo.loggedIn, self.clientInfo.getEvents(), 2, self.clientInfo.getPages())
            
            email = self.client_gui.ask_info(self.clientInfo.loggedIn, self.clientInfo.getEvents(), 9, self.clientInfo.getPages())
            
            args = [option,username,password,birthdate,email]

            response = self.requestServer(args)

            print(response)
            print(response['Message'])
        else:
            self.client_gui.invalid_info(self.clientInfo.loggedIn, 4)

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
