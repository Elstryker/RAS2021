import threading
import socket
import BookieLogic

SERVERHOST = ''
SERVERPORT = 40000

def main():
    sock = setupConnection()
    cl = BookieLogic.BookieLogic(sock)
    cl.run()

def setupConnection():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((SERVERHOST,SERVERPORT))
    sock.send("bookie".encode("utf-8"))
    print("Connected with server")
    return sock



if __name__ == "__main__":
    main()