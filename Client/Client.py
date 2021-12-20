import threading
import socket
import ClientLogic

SERVERHOST = ''
SERVERPORT = 40000

def main():
    sock = setupConnection()
    cl = ClientLogic.ClientLogic(sock)
    cl.run()

def setupConnection():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((SERVERHOST,SERVERPORT))
    print("Conectei-me com o servidor")
    return sock



if __name__ == "__main__":
    main()