class ClientInfo:

    loggedIn : bool
    wallet : dict[str,int] # Maps currency to total for example, "Euros":10
    events : list[dict] # List of events to print
    availableCurrencies : list # List of all of existing currencies in server
    detailedEvent : dict # Info for detailed event if user chooses to add bet


    def __init__(self,info) -> None:
        self.loggedIn = False
        self.wallet = dict()
        self.events = info["Events"]
        self.availableCurrencies = info["Currencies"]
        self.detailedEvent = dict()

    def updateInfo(self,wallet,events,detailedEvent,currencies):
        self.wallet = wallet
        self.events = events
        self.availableCurrencies = currencies
        self.detailedEvent = detailedEvent