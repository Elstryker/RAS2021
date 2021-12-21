import threading, socket, ServerWorkerClient, RASBetFacade, RASBetLN, ServerWorkerBookie
from Data import DataBaseAccess, MemoryDataBase

HOST = ''
PORT = 40000

def setupApplication():
    db : DataBaseAccess
    db = MemoryDataBase.MemoryDataBase()
    app : RASBetFacade
    app = RASBetLN.RASBetLN(db)
    return app

def main():
    app = setupApplication()
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST,PORT))
    sock.listen()
    while True:
        client_sock, info = sock.accept()
        data = client_sock.recv(256)
        message = data.decode("utf-8").strip()
        if message == 'client':
            sw = ServerWorkerClient.ServerWorkerClient(client_sock,info,app)
            print("Conectei-me com o cliente: ", info)
            sw.run()
        elif message == 'bookie':
            sw = ServerWorkerBookie.ServerWorkerBookie(client_sock,app)
            print("Conectei-me com o bookie: ", info)
            sw.run()


if __name__ == "__main__":
    main()