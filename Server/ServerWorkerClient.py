import threading
import socket
import RASBetFacade
import random, json

class ServerWorkerClient:

    sock : socket.socket
    info : dict
    app : RASBetFacade.RASBetFacade
    loggedIn : bool
    
    def __init__(self,sock,info,app : RASBetFacade.RASBetFacade):
        self.sock = sock
        self.info = info
        self.app = app
        self.eventPage = 0
        self.eventsPerPage = 5
        self.getIdForNotLoggedInUser()

    def getIdForNotLoggedInUser(self):
        self.loggedIn = False
        exist = True
        while exist:
            self.userID = random.randint(1,10000) # Not scalable
            result = self.app.getBetSlip(self.userID)
            dic = json.loads(result)
            exist = dic["Exists"]

    def run(self):
        self.sendInitialAppInfoToClient()
        threading.Thread(target=self.receiveClientRequests).start()

    def sendInitialAppInfoToClient(self):
        message = self.app.getDefaultInfo(self.userID)
        self.sock.send(message.encode("utf-8"))

    def receiveClientRequests(self):
        str_Data = ''
        while str_Data != 'S':
            data = self.sock.recv(256)
            str_Data = data.decode("utf-8")
            str_Data = str_Data.strip()
            if self.loggedIn:
                self.processRequestLoggedIn(str_Data)
            else:
                self.processRequestNotLoggedIn(str_Data)
        print("Bye!")
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

    def processRequestLoggedIn(self,req : str):
        tokens = req.split(";")
        operation = tokens[0]
        args = tokens[1:]
        message = ""
        #operation = int(operation)
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
            message = self.app.depositMoney(self.userID,args[0],args[1])
        elif operation == 7: # Withdraw Money
            message = self.app.withdrawMoney(self.userID,args[0],args[1])
        elif operation == 8: # Previous Page
            self.eventPage -= 1 if self.eventPage > 0 else self.eventPage
            self.app.getAvailableEvents(self.eventPage,self.eventsPerPage)
            message = "\n\nPrevious Page!\n"
        elif operation == 9: # Next Page
            self.eventPage += 1
            self.app.getAvailableEvents(self.eventPage,self.eventsPerPage)
            message = "\n\nNext Page!\n"
        elif operation == 10: # See Bet History
            message = self.app.getBetHistory(self.userID)
        elif operation == 11: # Register
            self.getIdForNotLoggedInUser()
            message = self.app.logout(self.userID)
        elif operation == 'S': # Quit
            replyBye = dict()
            replyBye['Message'] = "\nThank you for using RASBet, Bye!\n"
            message = json.dumps(replyBye)
        else:
            message = "Invalid input"
        self.sock.send(message.encode("utf-8"))


    def processRequestNotLoggedIn(self,req : str):
        tokens = req.split(";")
        operation = tokens[0]
        args = tokens[1:]
        message = ""
        #operation = int(operation)
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
        elif operation == 5: # Previous Page
            self.eventPage -= 1 if self.eventPage > 0 else self.eventPage
            self.app.getAvailableEvents(self.eventPage,self.eventsPerPage)
            message = "\n\nPrevious Page!\n"
        elif operation == 6: # Next Page
            self.eventPage += 1
            self.app.getAvailableEvents(self.eventPage,self.eventsPerPage)
            message = "\n\nNext Page!\n"
        elif operation == "F": # Login
            message = self.app.login(self.userID,args[0],args[1])
            dic = json.loads(message)
            if dic['LoggedIn']:
                self.userID = args[0] # username
                self.loggedIn = True
        elif operation == 8: # Register
            message = self.app.register(args[0],args[1],args[2])
        elif operation == 'S': # Quit
            replyBye = dict()
            replyBye['Message'] = "\nThank you for using RASBet, Bye!\n"
            message = json.dumps(replyBye)
        else:
            message = "Invalid input"
        self.sock.send(message.encode("utf-8"))