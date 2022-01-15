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