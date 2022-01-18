import threading, json
import socket
import ClientLogic

SERVERHOST = ''
SERVERPORT = 40000

def main():
    sock = setupConnection()
    info = getInitialAppInfoFromServer(sock)
    cl = ClientLogic.ClientLogic(sock,info)
    cl.run()

def getInitialAppInfoFromServer(sock):
    data = sock.recv(8192)
    data = data.decode("utf-8")
    info = json.loads(data)
    return info

def setupConnection():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((SERVERHOST,SERVERPORT))
    sock.send("client".encode("utf-8"))
    print("Connected with server")
    return sock



if __name__ == "__main__":
    main()