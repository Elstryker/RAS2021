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
        self.userID = 0
        
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
            pass
        if operation == 2: # Remove Bet From Bet Slip
            pass
        if operation == 3: # Cancel Bet Slip
            pass
        if operation == 4: # Show Bet Slip
            pass
        elif operation == 5: # Deposit Money
            self.app.depositMoney(self.userID,args[0],args[1])
            message = "\n\nMoney deposited with success!\n"
        if operation == 6: # Withdraw Money
            pass
        if operation == 7: # Previous Page
            pass
        if operation == 8: # Next Page
            pass
        if operation == 9: # Login
            pass
        else:
            message = "Invalid input"
        self.sock.send(message.encode("utf-8"))
