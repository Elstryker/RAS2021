from math import ceil

class ClientInfo:

    loggedIn : bool
    wallet : dict[str,int] # Maps currency to total for example, "Euros":10
    events : list[dict] # List of events to print
    availableCurrencies : list # List of all of existing currencies in server
    notifications : list



    def __init__(self,info) -> None:
        self.loggedIn = False
        self.wallet = dict()
        self.events = info["Events"]
        self.availableCurrencies = info["Currencies"]
        self.notifications = info["Notifications"]
        self.nonLoggedInBetSlip = []
        self.page = 0
        self.eventsPerPage = 2
        self.totalPages = ceil(len(self.events)/self.eventsPerPage)

    def updateInfo(self,response):
        self.wallet = response["Wallet"]
        self.events = response["Events"]
        self.availableCurrencies = response["Currencies"]
        self.notifications.extend(response["Notifications"])
        self.totalPages = ceil(len(self.events)/self.eventsPerPage)

    def nextPage(self):
        if self.page < self.totalPages - 1:
            self.page += 1

    def previousPage(self):
        self.page -= 1 if self.page > 0 else self.page

    def getEvents(self):
        offset = self.page * self.eventsPerPage
        events = self.events[offset:offset+self.eventsPerPage]
        return events

    def getNotifications(self,num):
        notifs = []
        if self.notifications == 0:
            return []

        if len(self.notifications) < num:
            num = len(self.notifications)

        for i in range(num):
            notifs.append(self.notifications.pop(0))
        
        return notifs

    def addBetNotLoggedIn(self,eventID,result):
        hasID = False
        eventID = int(eventID)
        result = int(result)
        for event in self.events:
            if eventID == int(event["Id"]):
                hasID = True
        
        if hasID:
            self.nonLoggedInBetSlip.append((eventID,result))
    
    def removeBetNotLoggedIn(self,eventID):
        eventID = int(eventID)

        for i,events in enumerate(self.nonLoggedInBetSlip):
            print(events)
            if events[0] == eventID:
                index = i
                break

        self.nonLoggedInBetSlip.pop(index)

    def cancelBetSlipNotLoggedIn(self):
        self.nonLoggedInBetSlip.clear()

    def getBetSlipNotLoggedIn(self):
        
        def getEvent(eventID):
            eve = None
            for event in self.events:
                if int(eventID) == int(event["Id"]):
                    hasID = True
                    eve = event

            return eve
        
        bets = []
        multOdd = 1
        for eventID,result in self.nonLoggedInBetSlip:
            betDict = dict()
            event = getEvent(eventID)
            betDict["EventID"] = eventID
            betDict["EventName"] = event["Name"]
            betDict["Choice"] = event["Intervenors"][result][1]
            betDict["Odd"] = event["Intervenors"][result][0]
            multOdd *= betDict["Odd"]
            bets.append(betDict)
            
        dictRet = dict()
        dictRet["Id"] = -1
        dictRet["Bets"] = bets
        dictRet["MultipliedOdd"] = multOdd
        dictRet["State"] = "Creating"

        return dictRet

    def getBetSlipNotLoggedInToSend(self):
        if len(self.nonLoggedInBetSlip) == 0:
            return "0"
        
        arrayTransform = []
        for eventID,result in self.nonLoggedInBetSlip:
            arrayTransform.append(f"{eventID},{result}")

        return ":".join(arrayTransform)