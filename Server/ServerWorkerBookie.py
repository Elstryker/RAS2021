import threading
import socket
import RASBetFacade
import random, json

class ServerWorkerBookie:

    sock : socket.socket
    info : dict
    app : RASBetFacade.RASBetFacade
    
    def __init__(self,sock,info,app : RASBetFacade.RASBetFacade):
        self.sock = sock
        self.info = info
        self.app = app

    def run(self):
        threading.Thread(target=self.receiveClientRequests).start()

    def receiveClientRequests(self):
        str_Data = ''
        while str_Data != '0':
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
        operation = int(operation)
        print("Operation:", operation)
        print("Args:", args)
        if operation == 1: # Add Event
            message = self.app.addEvent(args)
        elif operation == 2: # Add Sport
            message = self.app.addSport(args)
        elif operation == 3: # Add Intervenor
            message = self.app.addIntervenor(args)
        elif operation == 4: # Start Event
            message = self.app.startEvent(args)
        elif operation == 5: # Conclude Event
            message = self.app.concludeEvent(args)
        elif operation == 0: # Quit
            replyBye = dict()
            replyBye['Message'] = "\nThank you for using RASBet, Bye!\n"
            message = json.dumps(replyBye)
        else:
            message = "Invalid input"
        self.sock.send(message.encode("utf-8"))