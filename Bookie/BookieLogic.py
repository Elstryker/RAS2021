import socket
import json
import BookieGUI

class BookieLogic:
    
    sock : socket.socket

    def __init__(self,sock):
        self.sock = sock

    def menu(self):
        inp = ''
        while inp != '0':
            BookieGUI.showMenu()
            inp = input(" -> ")
            option = int(inp)
            self.handleInput(option)


    def requestServer(self,args) -> dict:
        message = ";".join(args)

        data = message.encode('utf-8')
        self.sock.send(data)
        data = self.sock.recv(2048)
        response = json.loads(data.decode('utf-8'))

        return response

    def handleInput(self,option): 
        option = str(option)
        actions = {
            "1":self.addEvent,
            "2":self.addSport,
            "3":self.addIntervenor,
            "4":self.startEvent,
            "5":self.concludeEvent,
            "0":self.quit
        }
        toDo = actions.get(option,self.noSuchAction)
        toDo(option)


    def getAndFillObjectParameters(self,option):
        args = [option,"GET"]
        reply = self.requestServer(args)
        params = reply["Params"]

        answers = []
        for key,value in params.items():
            if value == 0:
                BookieGUI.askParam(key)
                answer = input("-> ")
            elif isinstance(value, list):
                if key == "Intervenors":
                    BookieGUI.askLimitedParam(key,value,True) # To be able to choose more than one intervenor
                    answer = input("-> ").split(",")
                    answer = list(map(lambda x: value[int(x)-1],answer))
                    answer = ",".join(answer)
                else:
                    BookieGUI.askLimitedParam(key,value)
                    answer = int(input("-> "))
                    answer = value[answer-1]
            else:
                answer = ""
            answers.append(answer)

        return answers

    def addEvent(self,option):
        answers = self.getAndFillObjectParameters(option)

        args = [option,"PUT"]
        args.extend(answers)

        reply = self.requestServer(args)

        print(reply["Message"])

    def addSport(self,option):
        answers = self.getAndFillObjectParameters(option)

        args = [option,"PUT"]
        args.extend(answers)

        reply = self.requestServer(args)

        print(reply["Message"])

    def addIntervenor(self,option):
        answers = self.getAndFillObjectParameters(option)

        args = [option,"PUT"]
        args.extend(answers)

        reply = self.requestServer(args)

        print(reply["Message"])

    def startEvent(self,option):
        pass

    def concludeEvent(self,option):
        pass

    def noSuchAction(self,option):
        raise IOError
    
    def quit(self,option):
        args = [option]
        reply = self.requestServer(args)
        print(reply['Message'])

    def run(self):
        self.menu()
        self.closeConnection()

    def closeConnection(self):
        self.sock.close()
