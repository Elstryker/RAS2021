import threading
import socket
import RASBetFacade

class ServerWorkerClient:

    sock : socket.socket
    info : dict
    app : RASBetFacade.RASBetFacade
    userID : int
    
    def __init__(self,sock,info,app):
        self.sock = sock
        self.info = info
        self.app = app
        self.userID = -1
        self.eventPage = 0
        self.eventsPerPage = 5
        
    def run(self):
        self.sendInitialAppInfoToClient()
        threading.Thread(target=self.receiveClientRequests).start()

    def sendInitialAppInfoToClient(self):
        currencies = self.app.getCurrencies()
        separator = ','
        currencies = separator.join(currencies)
        self.sock.send(currencies.encode("utf-8"))

    def receiveClientRequests(self):
        while True:
            data = self.sock.recv(256)
            str_Data = data.decode("utf-8")
            str_Data = str_Data.strip()
            if str_Data == '0':
                break
            self.processRequest(str_Data)
        print("Bye!")
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

    def processRequest(self,req : str):
        tokens = req.split(" ")
        operation = tokens[0]
        args = tokens[1:]
        message = ""
        operation = int(operation)
        print("Operation:", operation)
        print("Args:", args)
        if operation == 1: # Add Bet To Bet Slip
            self.app.addBetToBetSlip(self.userID,args[0],args[1])
            message = "\n\nBet added with success!\n"
        elif operation == 2: # Remove Bet From Bet Slip
            self.app.removeBetFromBetSlip(self.userID,args[0])
            message = "\n\nBet removed with success!\n"
        elif operation == 3: # Cancel Bet Slip
            self.app.cancelBetSlip(self.userID)
            message = "\n\nCancelled Bet Slip with success!\n"
        elif operation == 4: # Show Bet Slip
            self.app.showBetSlip(self.userID)
            message = "\n\nSent Bet Slip!\n"
        elif operation == 5: # Conclude Bet Slip
            self.app.concludeBetSlip(self.userID,args[0],args[1])
            message = "\n\nMoney deposited with success!\n"
        elif operation == 6: # Deposit Money
            self.app.depositMoney(self.userID,args[0],args[1])
            message = "\n\nMoney deposited with success!\n"
        elif operation == 7: # Withdraw Money
            self.app.withdrawMoney(self.userID,args[0],args[1])
            message = "\n\nMoney withdrawed with success!\n"
        elif operation == 8: # Previous Page
            self.eventPage -= 1 if self.eventPage > 0 else self.eventPage
            self.app.getEvents(self.eventPage,self.eventsPerPage)
            message = "\n\nPrevious Page!\n"
        elif operation == 9: # Next Page
            self.eventPage += 1
            self.app.getEvents(self.eventPage,self.eventsPerPage)
            message = "\n\nNext Page!\n"
        elif operation == 10: # Login/Logout
            self.userID = self.app.login(args[0],args[1])
            message = "\n\nLogged in!\n"
        elif operation == 11: # Register
            message = self.app.register(args[0],args[1],args[2])
        else:
            message = "Invalid input"
        self.sock.send(message.encode("utf-8"))
