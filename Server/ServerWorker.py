import threading
import socket

class ServerWorker:

    sock : socket
    info : dict
    
    def __init__(self,sock,info):
        self.sock = sock
        self.info = info
        
    def run(self):
        threading.Thread(target=self.processClientRequests).start()

    def processClientRequests(self):
        while True:
            data = self.sock.recv(256)
            str_Data = data.decode("utf-8")
            print("Recebi: ", str_Data)
            if str_Data.strip() == '0':
                break
        print("Bye!")
        self.sock.close()
