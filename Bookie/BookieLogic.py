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
            "6":self.addCurrency,
            "7":self.removeCurrency,
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
                if key == "Odds":
                    BookieGUI.askParam("Odds for respective intervenors (if event permits draws, last odd is draw odd)")
                else:
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
        BookieGUI.askParam("Event id to start")
        eventID = input("-> ")

        args = [option,eventID]
        reply = self.requestServer(args)

        print(reply["Message"])

    def concludeEvent(self,option):
        args = [option,"GET"]
        reply = self.requestServer(args)
        
        if len(reply["Events"]) == 0:
            print("No events to conclude")
            return
        
        BookieGUI.printEvents(reply["Events"])

        BookieGUI.askParam("Event to start")
        eventID = int(input("-> "))

        event = reply["Events"][eventID]

        BookieGUI.askLimitedParam("Result",event["Intervenors"])
        result = input("-> ")

        args = [option,"PUT",str(event["Id"]),result]
        reply = self.requestServer(args)

        print(reply["Message"])

    def addCurrency(self,option):
        BookieGUI.askParam("Currency to add")
        currency = input("-> ")

        BookieGUI.askParam("Conversion to EUR")
        conversion = input("-> ")

        args = [option,currency,conversion]

        reply = self.requestServer(args)
        print(reply["Message"])

    def removeCurrency(self,option):
        BookieGUI.askParam(("Currency to remove"))

        currency = input("-> ")

        args = [option,currency]

        reply = self.requestServer(args)
        print(reply["Message"])

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
