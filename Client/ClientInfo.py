from math import ceil

class ClientInfo:

    loggedIn : bool
    wallet : dict[str,int] # Maps currency to total for example, "Euros":10
    events : list[dict] # List of events to print
    availableCurrencies : list # List of all of existing currencies in server


    def __init__(self,info) -> None:
        self.loggedIn = False
        self.wallet = dict()
        self.events = info["Events"]
        self.availableCurrencies = info["Currencies"]
        self.page = 0
        self.eventsPerPage = 2
        self.totalPages = ceil(len(self.events)/self.eventsPerPage)

    def updateInfo(self,wallet,events,currencies):
        self.wallet = wallet
        self.events = events
        self.availableCurrencies = currencies
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