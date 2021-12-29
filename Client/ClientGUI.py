import time
from os import name
from rich.console import Console
from rich.table import Table
from rich.layout import Layout
from rich.layout import Panel
from rich.text import Text
from rich.align import Align
from rich.columns import Columns
from rich.pretty import pprint

def showMenu(loggedIn : bool, console : Console, wallet : dict[str,int], events : list):
    layout : Layout = Layout()
    wallet : dict = {"EUR" : 42, "USD" : 69, "GBP" : 666, "ADA" : 420, "RASCoin" : 0}
    wallet_printable : str = ""
    
    
    events = [{"Name" : "Taça de Portugal", "Sport" : {"Name" : "Futebol", "Type" : "WinDraw"}, "Intervenors" : [(1.2, "Never gonna"), (2.2, "Give you up"), (1.8, "Draw")]}, 
    {"Name" : "Torneio Quim Fintas", "Sport" : {"Name" : "Golf", "Type" : "WinDraw"}, "Intervenors" : [(1.5, "Never gonna"), (3.2, "Let you down"), (1.2, "Draw")]},
    {"Name" : "Torneio Valério Belo", "Sport" : {"Name" : "Caricas", "Type" : "WinDraw"}, "Intervenors" : [(1.7, "Never gonna turn"), (4.1, "around and desert you"), (1.9, "Draw")]},
    {"Name" : "Taça António Costa", "Sport" : {"Name" : "Boa Bola", "Type" : "WinDraw"}, "Intervenors" : [(1.5, "He was a "), (3.2, "Sk8r boi"), (1.2, "Draw")]},
    {"Name" : "Campeonato José Figueiras", "Sport" : {"Name" : "Ping Pong", "Type" : "Win"}, "Intervenors" : [(1.5, "Belenenses"), (3.2, "Braga"), (1.2, "VITORIA")]}
    ]
    
    eventos_printable : list = showEvents(events)
    

    for currency, amount in wallet.items():
        wallet_printable+= f'{currency}: {amount}\n'


    
    """
    2 -> Remove Bet From Bet Slip
    3 -> Cancel Bet Slip
    4 -> Show Bet Slip
    5 -> Previous Page
    6 -> Next Page
    7 -> Login
    8 -> Register"""
    
    if not loggedIn:
        menu = [Panel("[red]E[/red]fetuar registo"), Panel("[red]F[/red]azer Login"), 
        Panel("[red]I[/red]ntroduzir Aposta"), Panel("[red]R[/red]emover Aposta"), 
        Panel("[red]C[/red]ancelar Boletim"), Panel("[red]M[/red]ostrar Boletim"), 
        Panel("[red]V[/red]alidar Boletim"), Panel("[red]D[/red]epositar Dinheiro"), 
        Panel("[red]L[/red]evantar Dinheiro"), Panel("Página [red]A[/red]nterior"), 
        Panel("[red]P[/red]róxima Página"), Panel("[red]S[/red]air")]
    else:
        menu = Text(
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
10 -> See Bet History
11 -> Logout""", justify = 'center')

    menu_printable = Columns(menu, equal=True, expand=True)

    rasbet_logo = Text("""
______  ___   ___________      _   
| ___ \/ _ \ /  ___| ___ \    | |  
| |_/ / /_\ \\  `--.| |_/ / ___| |_ 
|    /|  _  | `--. \ ___ \/ _ \ __|
| |\ \| | | |/\__/ / |_/ /  __/ |_ 
\_| \_\_| |_/\____/\____/ \___|\__|
""")                                   
    rasbet_logo.stylize("bold yellow")                                   

    logo_panel = Align(rasbet_logo, vertical='middle', align='center')
    balance_panel = Panel(Align(Text(wallet_printable, justify='center'), vertical='middle', align='center'), title='[red]Saldo')
    
    layout.split_column(
        Layout(" ", name="empty space"),
        Layout(name="header", ratio=2),
        Layout(Panel(eventos_printable, title='[red]Eventos'), name="events", ratio=6),
        Layout(Panel(menu_printable, title='[red]Menu'), name="menu", ratio=2)
    )

    layout["header"].split_row(
        Layout(logo_panel, name='logo', ratio = 8),
        Layout(balance_panel, name='balance', ratio = 1)
    )
 
    console.print(layout)
    #console.rule("[bold red]Menu")
    

    #time.sleep(2)
    #console.clear()

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

def showEvents(events : list):
    eventos_formatted = []
    
    for event in events:
        table_painel = Table()
        table_painel.add_column(Text(event["Sport"]["Name"], justify='center'))

        table = Table()

        table_painel.add_row(Text(event["Name"], justify='center'))

        intervenors = [x[1] for x in event["Intervenors"]]
        odds = [str(x[0]) for x in event["Intervenors"]]
        table.add_column(intervenors[0], justify="center", style="green", no_wrap=True)
            
        if event["Sport"]["Type"] == "WinDraw":
            intervenors.remove("Draw")
            drawOdd = odds.pop(-1)
            odds.insert(1,drawOdd)
            table.add_column("vs", justify="center", style="yellow", no_wrap=True)
            table.add_column(intervenors[1], justify="center", style="green", no_wrap=True)     
        else:
            table.add_column(intervenors[1], justify="center", style="green", no_wrap=True)
            table.add_column(intervenors[2], justify="center", style="green", no_wrap=True)     
        
        
        table.add_row(Text(odds[0], justify="center"), odds[1], odds[2])

        table_painel.add_row(table)

        eventos_formatted.append(table_painel)
        #string = " vs ".join(intervenors)
        #print(string)
        #string = " ; ".join(odds)
        #print(string)
        #print("______________________________")
    return Columns(eventos_formatted, equal=False, expand=True, align='center')