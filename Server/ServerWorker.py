import threading
import socket
import RASBetFacade

class ServerWorker:

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
        threading.Thread(target=self.receiveClientRequests).start()

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
        if operation == 1:
            self.app.depositMoney(self.userID,args[0])
            message = "\n\nMoney deposited with success!\n"
        else:
            message = "Invalid input"
        self.sock.send(message.encode("utf-8"))
