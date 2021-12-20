import socket 

class ClientLogic:
    
    def __init__(self,sock):
        self.sock = sock

    def run(self):
        print("Defina a mensagem a enviar ou insira 0 para encerrar!")
        inp = ''
        while inp != '0':
            inp = input(" -> ")
            data = inp.encode('utf-8')
            self.sock.send(data)
        self.closeConnection()

    def closeConnection(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
