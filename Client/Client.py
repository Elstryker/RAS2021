import threading
import socket
import ClientLogic

SERVERHOST = ''
SERVERPORT = 40000

def main():
    sock = setupConnection()
    info = getInitialAppInfoFromServer(sock)
    cl = ClientLogic.ClientLogic(sock,info["Currencies"])
    cl.run()

def getInitialAppInfoFromServer(sock):
    data = sock.recv(256)
    currencies = data.decode("utf-8")
    currencies = currencies.split(",")
    info = dict()
    info["Currencies"] = currencies
    return info

def setupConnection():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((SERVERHOST,SERVERPORT))
    sock.send("client".encode("utf-8"))
    print("Conectei-me com o servidor")
    return sock



if __name__ == "__main__":
    main()