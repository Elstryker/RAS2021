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
            exist = dic["Success"]

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
            self.processRequest(str_Data)
        print("Bye!")
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

    def processRequest(self,req : str):
        tokens = req.split(";")
        operation = tokens[0]
        args = tokens[1:]
        message = ""
        #operation = int(operation)
        print("Operation:", operation)
        print("Args:", args)
        if operation == "I": # Add Bet To Bet Slip
            message = self.app.addBetToBetSlip(self.userID,args)
        elif operation == "R": # Remove Bet From Bet Slip
            message = self.app.removeBetFromBetSlip(self.userID,args[0])
        elif operation == "C": # Cancel Bet Slip
            message = self.app.cancelBetSlip(self.userID)
        elif operation == "M": # Show Bet Slip
            message = self.app.getBetSlip(self.userID)
        elif operation == "V": # Conclude Bet Slip
            message = self.app.concludeBetSlip(self.userID,args[0],args[1])
        elif operation == 'D': # Deposit Money
            message = self.app.depositMoney(self.userID,args[0],args[1])
        elif operation == 'L': # Withdraw Money
            message = self.app.withdrawMoney(self.userID,args[0],args[1])
        elif operation == "H": # See Bet History
            message = self.app.getBetHistory(self.userID)
        elif operation == "E": # Register
            message = self.app.register(args[0],args[1],args[2])
        elif operation == "F": # Login
            message = self.app.login(self.userID,args[0],args[1])
            dic = json.loads(message)
            if dic['LoggedIn']:
                self.userID = args[0] # username
                self.loggedIn = True
        elif operation == 'O': # Logout
            self.getIdForNotLoggedInUser()
            message = self.app.logout(self.userID)
        elif operation == 'S': # Quit
            replyBye = dict()
            replyBye['Message'] = "\nThank you for using RASBet, Bye!\n"
            message = json.dumps(replyBye)
        else:
            message = "Invalid input"
        self.sock.send(message.encode("utf-8"))