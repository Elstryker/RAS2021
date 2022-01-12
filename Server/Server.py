import threading, socket, ServerWorkerClient, RASBetFacade, RASBetLN, ServerWorkerBookie

from sqlalchemy_utils.functions.database import database_exists
from Data.Database import Base
from Data import DataBaseAccess,Database

HOST = ''
PORT = 40000

def setupApplication():
    db : DataBaseAccess
    db = Database.DataBase()
    app : RASBetFacade
    app = RASBetLN.RASBetLN(db)

    Base.metadata.create_all(bind=db.engine)

    if not database_exists(db.engine.url):
            print("Creating db")
            db.create_database(db.engine.url)
    print("Creating tables")
    Base.metadata.create_all(db.engine)

    print("Initialized the db")

    #db.createDefault()
    return app

def main():
    app = setupApplication()
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST,PORT))
    sock.listen()
    while True:
        client_sock, info = sock.accept()
        threading.Thread(target=runServerWorker,args=[client_sock,info,app]).start()


        
def runServerWorker(client_sock,info,app):
    data = client_sock.recv(256)
    message = data.decode("utf-8").strip()
    if message == 'client':
        sw = ServerWorkerClient.ServerWorkerClient(client_sock,info,app)
        print("Conectei-me com o cliente: ", info)
        sw.run()
    elif message == 'bookie':
        sw = ServerWorkerBookie.ServerWorkerBookie(client_sock,info,app)
        print("Conectei-me com o bookie: ", info)
        sw.run()

if __name__ == "__main__":
    main()