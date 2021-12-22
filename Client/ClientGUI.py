def showMenu(loggedIn : bool):
    if not loggedIn:
        print(
"""
0 -> Quit
1 -> Add Bet To Bet Slip
2 -> Remove Bet From Bet Slip
3 -> Cancel Bet Slip
4 -> Show Bet Slip
5 -> Conclude Bet Slip
6 -> Deposit Money
7 -> Withdraw Money
8 -> Previous Page
9 -> Next Page
10 -> Login
11 -> Register""")
    else:
        print(
"""
0 -> Quit
1 -> Add Bet To Bet Slip
2 -> Remove Bet From Bet Slip
3 -> Cancel Bet Slip
4 -> Show Bet Slip
5 -> Conclude Bet Slip
6 -> Deposit Money
7 -> Withdraw Money
8 -> Previous Page
9 -> Next Page
10 -> Logout""")

def askAmount():
    print(
"""
Amount:""")

def askCurrency(availableCurrencies):
    print(
"""
Choose currency:""")
    for i,el in enumerate(availableCurrencies):
        print(f"{i+1} - {el}")

def askEvent():
    print("Which event?")

def showDetailedEvent():
    print(
"""
0 - Empate
1 - Vitória
2 - Derrota
""")

def askUserName():
    print("Enter Username:")

def askPassword():
    print("Enter Password:")

def askBirthDate():
    print("Enter Birthdate (dd/mm/yyyy):")
