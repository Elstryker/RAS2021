import threading
import socket
import ServerWorker

HOST = ''
PORT = 40000

def main():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST,PORT))
    sock.listen()
    while True:
        client_sock, info = sock.accept()
        print("Conectei-me com o cliente: ", info)
        sw = ServerWorker.ServerWorker(client_sock,info)
        sw.run()


if __name__ == "__main__":
    main()