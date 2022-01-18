from math import ceil

class ClientInfo:

    loggedIn : bool
    wallet : dict[str,int] # Maps currency to total for example, "Euros":10
    events : list[dict] # List of events to print
    availableCurrencies : list # List of all of existing currencies in server
    notifications : list
    filtros : list
    filtros_ativos : list

    def __init__(self,info) -> None:
        self.loggedIn = False
        self.wallet = dict()
        self.events = info["Events"]
        self.availableCurrencies = info["Currencies"]
        self.notifications = info["Notifications"]
        self.page = 0
        self.eventsPerPage = 3
        self.totalPages = ceil(len(self.events)/self.eventsPerPage)
        self.filtros = ["WinDraw", "Win", "Futebol", "Tenis", "Corrida", "Golf", "Ping Pong"]
        self.filtros_ativos = ["WinDraw", "Win", "Futebol", "Tenis", "Corrida", "Golf", "Ping Pong"]
    

    def updateInfo(self,response):
        self.wallet = response["Wallet"]
        self.events = response["Events"]
        self.availableCurrencies = response["Currencies"]
        self.notifications.extend(response["Notifications"])
        self.totalPages = ceil(len(self.events)/self.eventsPerPage)

    def getPages(self):
        return self.page,self.totalPages
    

    def getFiltros(self):
        return self.filtros

    def getFiltros_ativos(self):
        return self.filtros_ativos

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
        if not self.notifications:
            #print("well nao ha nada")
            return []

        if len(self.notifications) < num:
            num = len(self.notifications)

        #print(num)
        for i in range(num):
            notifs.append(self.notifications.pop(0))
        
        

        return notifs