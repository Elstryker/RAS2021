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

class ClientGUI:
    console : Console
    questions : list
    username : str
    wallet : dict

    def __init__(self):
        self.console = Console()
        self.username = None
        self.questions = list()
        self.questions.append(Text("""
  _____       _                 _                          _    _                                              
 |_   _|     | |               | |                        | |  | |                                           _ 
   | |  _ __ | |_ _ __ ___   __| |_   _ ______ _    ___   | |  | |___  ___ _ __ _ __   __ _ _ __ ___   ___  (_)
   | | | '_ \| __| '__/ _ \ / _` | | | |_  / _` |  / _ \  | |  | / __|/ _ \ '__| '_ \ / _` | '_ ` _ \ / _ \    
  _| |_| | | | |_| | | (_) | (_| | |_| |/ / (_| | | (_) | | |__| \__ \  __/ |  | | | | (_| | | | | | |  __/  _ 
 |_____|_| |_|\__|_|  \___/ \__,_|\__,_/___\__,_|  \___/   \____/|___/\___|_|  |_| |_|\__,_|_| |_| |_|\___| (_)                                                                                                                                                                                                                           
                    """))
        self.questions.append(Text("""
  _____       _                 _                          _____                                    _     
 |_   _|     | |               | |                        |  __ \                                  | |  _ 
   | |  _ __ | |_ _ __ ___   __| |_   _ ______ _    __ _  | |__) |_ _ ___ _____      _____  _ __ __| | (_)
   | | | '_ \| __| '__/ _ \ / _` | | | |_  / _` |  / _` | |  ___/ _` / __/ __\ \ /\ / / _ \| '__/ _` |    
  _| |_| | | | |_| | | (_) | (_| | |_| |/ / (_| | | (_| | | |  | (_| \__ \__ \\\ V  V / (_) | | | (_| |  _ 
 |_____|_| |_|\__|_|  \___/ \__,_|\__,_/___\__,_|  \__,_| |_|   \__,_|___/___/ \_/\_/ \___/|_|  \__,_| (_)
                                                                                                          
                                                                                                          
"""))
        self.questions.append(Text("""
  _____        _              _                             _                      _           __   _     _     __                      __                   __      
 |  __ \      | |            | |                           (_)                    | |         / /  | |   | |   / /                     / /                   \ \   _ 
 | |  | | __ _| |_ __ _    __| | ___   _ __   __ _ ___  ___ _ _ __ ___   ___ _ __ | |_ ___   | | __| | __| |  / / __ ___  _ __ ___    / /_ _  __ _  __ _  __ _| | (_)
 | |  | |/ _` | __/ _` |  / _` |/ _ \ | '_ \ / _` / __|/ __| | '_ ` _ \ / _ \ '_ \| __/ _ \  | |/ _` |/ _` | / / '_ ` _ \| '_ ` _ \  / / _` |/ _` |/ _` |/ _` | |    
 | |__| | (_| | || (_| | | (_| |  __/ | | | | (_| \__ \ (__| | | | | | |  __/ | | | || (_) | | | (_| | (_| |/ /| | | | | | | | | | |/ / (_| | (_| | (_| | (_| | |  _ 
 |_____/ \__,_|\__\__,_|  \__,_|\___| |_| |_|\__,_|___/\___|_|_| |_| |_|\___|_| |_|\__\___/  | |\__,_|\__,_/_/ |_| |_| |_|_| |_| |_/_/ \__,_|\__,_|\__,_|\__,_| | (_)
                                                                                              \_\                                                            /_/     
                                                                                                                                                                     
"""))
        self.questions.append(Text("""
  _____           _                     __  __             _              _           
 |_   _|         (_)                   |  \/  |           | |            | |        _ 
   | |  _ __  ___ _ _ __ __ _    ___   | \  / | ___  _ __ | |_ __ _ _ __ | |_ ___  (_)
   | | | '_ \/ __| | '__/ _` |  / _ \  | |\/| |/ _ \| '_ \| __/ _` | '_ \| __/ _ \    
  _| |_| | | \__ \ | | | (_| | | (_) | | |  | | (_) | | | | || (_| | | | | ||  __/  _ 
 |_____|_| |_|___/_|_|  \__,_|  \___/  |_|  |_|\___/|_| |_|\__\__,_|_| |_|\__\___| (_)
                                                                                      
                                                                                      
"""))
        self.questions.append(Text("""
 _____      _                 _                                               _              _                _           _           
|_   _|    | |               | |                                             | |            | |              (_)         | |        _ 
  | | _ __ | |_ _ __ ___   __| |_   _ ______ _    ___     _____   _____ _ __ | |_ ___     __| | ___  ___  ___ _  __ _  __| | ___   (_)
  | || '_ \| __| '__/ _ \ / _` | | | |_  / _` |  / _ \   / _ \ \ / / _ \ '_ \| __/ _ \   / _` |/ _ \/ __|/ _ \ |/ _` |/ _` |/ _ \     
 _| || | | | |_| | | (_) | (_| | |_| |/ / (_| | | (_) | |  __/\ V /  __/ | | | || (_) | | (_| |  __/\__ \  __/ | (_| | (_| | (_) |  _ 
 \___/_| |_|\__|_|  \___/ \__,_|\__,_/___\__,_|  \___/   \___| \_/ \___|_| |_|\__\___/   \__,_|\___||___/\___| |\__,_|\__,_|\___/  (_)
                                                                                                            _/ |                      
                                                                                                           |__/                       
"""))

        self.questions.append(Text("""
  _____                   _                                       _                          _            _           
 |  __ \                 (_)                                     | |                        | |          | |        _ 
 | |__) | __ ___  ___ ___ _  ___  _ __   ___     __ _ _   _  __ _| | __ _ _   _  ___ _ __   | |_ ___  ___| | __ _  (_)
 |  ___/ '__/ _ \/ __/ __| |/ _ \| '_ \ / _ \   / _` | | | |/ _` | |/ _` | | | |/ _ \ '__|  | __/ _ \/ __| |/ _` |    
 | |   | | |  __/\__ \__ \ | (_) | | | |  __/  | (_| | |_| | (_| | | (_| | |_| |  __/ |     | ||  __/ (__| | (_| |  _ 
 |_|   |_|  \___||___/___/_|\___/|_| |_|\___|   \__, |\__,_|\__,_|_|\__, |\__,_|\___|_|      \__\___|\___|_|\__,_| (_)
                                                   | |                 | |                                            
                                                   |_|                 |_|                                            
"""))
        self.questions.append(Text("""
 _____          _                     ___________       _                               _            
|_   _|        (_)                   |_   _|  _  \     | |                             | |         _ 
  | | _ __  ___ _ _ __ __ _    ___     | | | | | |   __| | __ _    __ _ _ __   ___  ___| |_ __ _  (_)
  | || '_ \/ __| | '__/ _` |  / _ \    | | | | | |  / _` |/ _` |  / _` | '_ \ / _ \/ __| __/ _` |    
 _| || | | \__ \ | | | (_| | | (_) |  _| |_| |/ /  | (_| | (_| | | (_| | |_) | (_) \__ \ || (_| |  _ 
 \___/_| |_|___/_|_|  \__,_|  \___/   \___/|___/    \__,_|\__,_|  \__,_| .__/ \___/|___/\__\__,_| (_)
                                                                       | |                           
                                                                       |_|                           
"""))
        self.questions.append(Text("""
 _____          _                     ___________       _        ______       _      _   _           
|_   _|        (_)                   |_   _|  _  \     | |       | ___ \     | |    | | (_)          
  | | _ __  ___ _ _ __ __ _    ___     | | | | | |   __| | ___   | |_/ / ___ | | ___| |_ _ _ __ ___  
  | || '_ \/ __| | '__/ _` |  / _ \    | | | | | |  / _` |/ _ \  | ___ \/ _ \| |/ _ \ __| | '_ ` _ \ 
 _| || | | \__ \ | | | (_| | | (_) |  _| |_| |/ /  | (_| | (_) | | |_/ / (_) | |  __/ |_| | | | | | |
 \___/_| |_|___/_|_|  \__,_|  \___/   \___/|___/    \__,_|\___/  \____/ \___/|_|\___|\__|_|_| |_| |_|
                                                                                                     
                                                                                                     
"""))
        self.questions.append(Text("""      
 _____              __ _                                                ______                                   _      
/  __ \            / _(_)                                               | ___ \                                 | |  _  
| /  \/ ___  _ __ | |_ _ _ __ _ __ ___   ___    __ _   ___ _   _  __ _  | |_/ /_ _ ___ _____      _____  _ __ __| | (_) 
| |    / _ \| '_ \|  _| | '__| '_ ` _ \ / _ \  / _` | / __| | | |/ _` | |  __/ _` / __/ __\ \ /\ / / _ \| '__/ _` |     
| \__/\ (_) | | | | | | | |  | | | | | |  __/ | (_| | \__ \ |_| | (_| | | | | (_| \__ \__ \\\ V  V / (_) | | | (_| |  _  
 \____/\___/|_| |_|_| |_|_|  |_| |_| |_|\___|  \__,_| |___/\__,_|\__,_| \_|  \__,_|___/___/ \_/\_/ \___/|_|  \__,_| (_) 
                                                                                                                        
                                                                                                                        
"""))
        self.questions.append(Text("""
 _____          _                                                           _ _     
|_   _|        (_)                                                         (_) |  _ 
  | | _ __  ___ _ _ __ __ _    ___    ___  ___ _   _    ___ _ __ ___   __ _ _| | (_)
  | || '_ \/ __| | '__/ _` |  / _ \  / __|/ _ \ | | |  / _ \ '_ ` _ \ / _` | | |    
 _| || | | \__ \ | | | (_| | | (_) | \__ \  __/ |_| | |  __/ | | | | | (_| | | |  _ 
 \___/_| |_|___/_|_|  \__,_|  \___/  |___/\___|\__,_|  \___|_| |_| |_|\__,_|_|_| (_)
"""))                                                                                    
                                                                                    
 
   
    def goodbye(self):
        layout : Layout = Layout()
        
        goodbye_text = Text("""
   ____  _          _                 _                                                _ _                
  / __ \| |        (_)               | |                                              | | |               
 | |  | | |__  _ __ _  __ _  __ _  __| | ___    _ __   ___  _ __    ___  ___  ___ ___ | | |__   ___ _ __  
 | |  | | '_ \| '__| |/ _` |/ _` |/ _` |/ _ \  | '_ \ / _ \| '__|  / _ \/ __|/ __/ _ \| | '_ \ / _ \ '__| 
 | |__| | |_) | |  | | (_| | (_| | (_| | (_) | | |_) | (_) | |    |  __/\__ \ (_| (_) | | | | |  __/ |    
  \____/|_.__/|_|  |_|\__, |\__,_|\__,_|\___/  | .__/ \___/|_|     \___||___/\___\___/|_|_| |_|\___|_|    
                       __/ |    _____          | |_____ ____  ______ _______                              
                      |___/    |  __ \     /\  |_/ ____|  _ \|  ____|__   __|                             
                               | |__) |   /  \  | (___ | |_) | |__     | |                                
                               |  _  /   / /\ \  \___ \|  _ <|  __|    | |                                
                               | | \ \  / ____ \ ____) | |_) | |____   | |                                
                               |_|  \_\/_/    \_\_____/|____/|______|  |_|                                
                                                                                                          
                                                                                                          
""")
        goodbye_text.stylize("bold yellow")

        layout.split_column(
            Layout(" ", name="empty space", ratio=3),
            Layout(Align(goodbye_text, align='center'), ratio=3)
        )

        self.console.print(layout)

    def invalid_info(self, loggedIn, opcao : int):
            self.console.clear()
            mensagem = list()

            mensagem.append(self.questions[5])
            mensagem.append(Text("""
  ______                _                 _                             __                      
 |  ____|              | |               (_)                           / _|                     
 | |__ __ _  ___ __ _  | |     ___   __ _ _ _ __    _ __   ___  _ __  | |_ __ ___   _____  _ __ 
 |  __/ _` |/ __/ _` | | |    / _ \ / _` | | '_ \  | '_ \ / _ \| '__| |  _/ _` \ \ / / _ \| '__|
 | | | (_| | (_| (_| | | |___| (_) | (_| | | | | | | |_) | (_) | |    | || (_| |\ V / (_) | |   
 |_|  \__,_|\___\__,_| |______\___/ \__, |_|_| |_| | .__/ \___/|_|    |_| \__,_| \_/ \___/|_|   
             )_)                     __/ |         | |                                          
                                    |___/          |_|                                          
"""))

            mensagem.append(Text("""
   _____            _               _____             __  _ _     _                
  |  __ \          | |             |_   _|           /_/ | (_)   | |               
  | |  | | __ _  __| | ___  ___      | |  _ ____   ____ _| |_  __| | ___  ___      
  | |  | |/ _` |/ _` |/ _ \/ __|     | | | '_ \ \ / / _` | | |/ _` |/ _ \/ __|     
  | |__| | (_| | (_| | (_) \__ \    _| |_| | | \ V / (_| | | | (_| | (_) \__ \     
  |_____/ \__,_|\__,_|\___/|___/   |_____|_| |_|\_/ \__,_|_|_|\__,_|\___/|___/     
   _______         _                                                       _       
  |__   __|       | |                                                     | |      
     | | ___ _ __ | |_ ___      _ __   _____   ____ _ _ __ ___   ___ _ __ | |_ ___ 
     | |/ _ \ '_ \| __/ _ \    | '_ \ / _ \ \ / / _` | '_ ` _ \ / _ \ '_ \| __/ _ \\
     | |  __/ | | | ||  __/    | | | | (_) \ V / (_| | | | | | |  __/ | | | ||  __/
     |_|\___|_| |_|\__\___|    |_| |_|\___/ \_/ \__,_|_| |_| |_|\___|_| |_|\__\___|
                                                                                   
                                                                                   
"""))

            mensagem.append(Text("""

 _   _            _                                           _ _            _                                    _                 _       
| \ | |          | |                                         | | |          | |                                  | |               | |      
|  \| | ___ _ __ | |__  _   _ _ __ ___    _ __ ___  ___ _   _| | |_ __ _  __| | ___     ___ _ __   ___ ___  _ __ | |_ _ __ __ _  __| | ___  
| . ` |/ _ \ '_ \| '_ \| | | | '_ ` _ \  | '__/ _ \/ __| | | | | __/ _` |/ _` |/ _ \   / _ \ '_ \ / __/ _ \| '_ \| __| '__/ _` |/ _` |/ _ \ 
| |\  |  __/ | | | | | | |_| | | | | | | | | |  __/\__ \ |_| | | || (_| | (_| | (_) | |  __/ | | | (_| (_) | | | | |_| | | (_| | (_| | (_) |
\_| \_/\___|_| |_|_| |_|\__,_|_| |_| |_| |_|  \___||___/\__,_|_|\__\__,_|\__,_|\___/   \___|_| |_|\___\___/|_| |_|\__|_|  \__,_|\__,_|\___/ 
                                                                                                                                            
                                                                                                                                            
                                                                              
"""))
            mensagem.append(Text("""
______                                   _           _ _  __                    _            
| ___ \                                 | |         | (_)/ _|                  | |           
| |_/ /_ _ ___ _____      _____  _ __ __| |___    __| |_| |_ ___ _ __ ___ _ __ | |_ ___  ___ 
|  __/ _` / __/ __\ \ /\ / / _ \| '__/ _` / __|  / _` | |  _/ _ \ '__/ _ \ '_ \| __/ _ \/ __|
| | | (_| \__ \__ \\\ V  V / (_) | | | (_| \__ \ | (_| | | ||  __/ | |  __/ | | | ||  __/\__ \\
\_|  \__,_|___/___/ \_/\_/ \___/|_|  \__,_|___/  \__,_|_|_| \___|_|  \___|_| |_|\__\___||___/
"""))                                                                                             
                                                                                             


            for elem in mensagem:
                elem.stylize("bold red")
                                                                              

            layout : Layout = Layout()

            layout.split_column(
                Layout(" ", name="empty space"),
                Layout(name="header", ratio=3),
                Layout(Panel(Align(mensagem[opcao], align='center', vertical="middle")), ratio=9),
                Layout(mensagem[0], ratio=3)
            )

            self.login_layout(loggedIn, layout)

            self.console.print(layout)
            answer = self.console.input("-> ")
    
    def show_history_betslips(self, betslips :list):
        eventos_formatted = []
        
        print(betslips)

        for betslip in betslips:
            table_painel =  Table()
            texto = Text(str(betslip["Id"]) + " | " + f"Apostas: {len(betslip['Bets'    ])}" , justify='center')
            texto.stylize("red", 0, 2)
            table_painel.add_column(texto)
            
            table = Table()

            table.add_column("Estado", justify="center", style="cyan", no_wrap=True)
            table.add_column("Valor Total", justify="center", style="bold yellow", no_wrap=True)
            
            print(betslip["State"])

            if betslip["State"] == "InCourse":
                estado = Text("A decorrer")
                estado.stylize("bold green")
            else:
                estado = Text("Finalizado")
                estado.stylize("red")

            table.add_row(estado, str(betslip["InStake"]))

            table_painel.add_row(table)

            eventos_formatted.append(table_painel)
        

        return Columns(eventos_formatted, equal=False, align='center')

    def show_history(self, loggedIn, betslips : list):
        self.console.clear()

        layout : Layout = Layout()

        prompt = self.questions[7]
        prompt.stylize("bold yellow")

        eventos_printable : list = self.show_history_betslips(betslips)
        
        layout.split_column(
            Layout(" ", name="empty space"),
            Layout(name="header", ratio=3),
            Layout(Panel(eventos_printable, title='[red]Histórico'), name="events", ratio=8),
            Layout(Align(prompt, align='center'), name="menu", ratio=3)
        )

        self.login_layout(loggedIn, layout)

        self.console.print(layout)

        return self.console.input("->")
 
    def show_betslip_detail(self, loggedIn, events, opcao):
        self.console.clear()

        print(events)
        layout : Layout = Layout()

        prompt = self.questions[opcao]
        prompt.stylize("bold yellow")

        eventos_printable : list = self.showEventsSlip(events["BetSlip"]['Bets'])
        
        if events["BetSlip"]['MultipliedOdd'] == '1':
            odd_final = 0
        else:
            odd_final = events["BetSlip"]['MultipliedOdd']

        layout.split_column(
            Layout(" ", name="empty space"),
            Layout(name="header", ratio=3),
            Layout(Panel(eventos_printable, title='[red]Boletim'), name="events", ratio=8),
            Layout(Align("[bold yellow] ODD FINAL:[/bold yellow] " + str(odd_final), align='center')),
            Layout(Align(prompt, align='center'), name="menu", ratio=3)
        )

        self.login_layout(loggedIn, layout)

        self.console.print(layout)

        return self.console.input("->")

    def ask_info(self, loggedIn : bool, events : list, question : int, paginas):
        answer = ''
        eventos_printable : list = self.showEvents(events)
        prompt = self.questions[question]
                
        prompt.stylize("bold yellow")                                                                                       
                                                                                                           

        while answer == '':
            self.console.clear()
            layout : Layout = Layout()
        
            layout.split_column(
                Layout(" ", name="empty space"),
                Layout(name="header", ratio=3),
                Layout(Panel(eventos_printable, title=f'[red]Eventos[/red] - [bold yellow]Página {paginas[0]+1}/{paginas[1]}'), name="events", ratio=9),
                Layout(prompt, ratio=3)
            )

            self.login_layout(loggedIn, layout)

            self.console.print(layout)
            answer = self.console.input("-> ")
        return answer
    
    def login_layout(self, loggedIn : bool, layout : Layout, notificacoes=None):
        logo_panel = self.get_logo_panel()

        if not loggedIn:
            layout["header"].split_row(
                Layout(logo_panel, name='logo', ratio = 8), 
                Layout(" ", ratio=2),
                Layout(" ", name='balance', ratio = 1)
            )
        else:
            
            wallet_printable : str = ""
            
            for currency, amount in self.wallet.items():
                wallet_printable+= f'{currency}: {amount}\n'

            balance_panel = Panel(Align(Text(wallet_printable, justify='center'), vertical='middle', align='center'), title='[red]Saldo')

            
            
  
            if notificacoes:
                layout["header"].split_row(
                    Layout(name="notificacoes", ratio=2),
                    Layout(logo_panel, name='logo', ratio = 6),
                    Layout(name="login", ratio=2),
                    Layout(balance_panel, name='balance', ratio = 1)
                )

                notif1 = self.get_mensagem(notificacoes[0])

                if len(notificacoes) == 1:
                    layout["notificacoes"].split_column(
                        Layout(Panel(Align(notif1,vertical='middle', align='center'), title='[red]Notificação'))
                    )
                else:
                    notif2 = Text("Perdeu uma aposta!")
                    notif2.stylize("red", 0, 6)

                    layout["notificacoes"].split_column(
                        Layout(Panel(Align(notif1,vertical='middle', align='center'), title='[red]Notificação')),
                        Layout(Panel(Align(notif2,vertical='middle', align='center'), title='[red]Notificação'))
                    )
            else:
                layout["header"].split_row(
                    Layout(logo_panel, name='logo', ratio = 8),
                    Layout(name="login", ratio=2),
                    Layout(balance_panel, name='balance', ratio = 1)
                )

            logout = Text("Logout", justify='center')
            logout.stylize("red", 1,2)

            layout["login"].split_column(
                Layout(Panel(Align(logout,vertical='middle', align='center'))),
                Layout(Panel(Align(Text(self.username, justify='center'),vertical='middle', align='center'), title='[red]Username'))
            )

    def get_mensagem(self, mensagem):
        if mensagem[0] == 0:
            resposta = Text("Perdeu uma aposta!")
            resposta.stylize("red", 0, 6)
        else:
            resposta = Text(f"Ganhou {mensagem[1][0]} {mensagem[1][1]} numa aposta!")
            resposta.stylize("bold green", 0,6)
             
        return resposta
    
    def get_logo_panel(self):
        rasbet_logo = Text("""
    ______  ___   ___________      _   
    | ___ \/ _ \ /  ___| ___ \    | |  
    | |_/ / /_\ \\\ `--.| |_/ / ___| |_ 
    |    /|  _  | `--. \ ___ \/ _ \ __|
    | |\ \| | | |/\__/ / |_/ /  __/ |_ 
    \_| \_\_| |_/\____/\____/ \___|\__|
    """)                                   
        rasbet_logo.stylize("bold yellow")                                   

        logo_panel = Align(rasbet_logo, vertical='middle', align='center')

        return logo_panel

    

    def pede_moeda(self, loggedIn, events : list, currencies : list, conclude : bool, paginas, opcao = 0):
        self.console.clear()
        layout : Layout = Layout()
        
        currencies = [Panel(Align(Text(currency, tab_size=8), align='center'), title=f'[red]{index}[/red]') for index,currency in enumerate(currencies)]

        moedas_printable = Columns(currencies, equal=False, expand=True)
        
        if conclude:
            eventos_printable : list = self.showEventsSlip(events["BetSlip"]['Bets'])
            
            layout.split_column(
                Layout(" ", name="empty space"),
                Layout(name="header", ratio=3),
                Layout(Panel(eventos_printable, title='[red]Boletim'), name="events", ratio=8),
                Layout(Align("[bold yellow] ODD FINAL:[/bold yellow] " + str(events["BetSlip"]['MultipliedOdd']), align='center')),
                Layout(Panel(moedas_printable, title='[red]Menu'), name="menu", ratio=3)
            )
        else:    
            eventos_printable : list = self.showEvents(events)
            
            if opcao == 0:
                layout.split_column(
                    Layout(" ", name="empty space"),
                    Layout(name="header", ratio=3),
                    Layout(Panel(eventos_printable, title=f'[red]Eventos[/red] - [bold yellow]Página {paginas[0]+1}/{paginas[1]}'), name="events", ratio=9),
                    Layout(Panel(moedas_printable, title='[red]Menu'), name="menu", ratio=3)
                )
            elif opcao == 1:
                layout.split_column(
                    Layout(" ", name="empty space"),
                    Layout(name="header", ratio=3),
                    Layout(Panel(eventos_printable, title=f'[red]Eventos[/red] - [bold yellow]Página {paginas[0]+1}/{paginas[1]}'), name="events", ratio=9),
                    Layout(Panel(moedas_printable, title='[red]Moeda que deseja converter'), name="menu", ratio=3)
                )
            else:
                layout.split_column(
                    Layout(" ", name="empty space"),
                    Layout(name="header", ratio=3),
                    Layout(Panel(eventos_printable, title=f'[red]Eventos[/red] - [bold yellow]Página {paginas[0]+1}/{paginas[1]}'), name="events", ratio=9),
                    Layout(Panel(moedas_printable, title='[red]Moeda que deseja obter'), name="menu", ratio=3)
                )

        self.login_layout(loggedIn, layout)

        self.console.print(layout)

        return self.console.input("Introduza o número da opção desejada -> ")
 

    def show_betslip(self, loggedIn, events, opcao):
        self.console.clear()

        layout : Layout = Layout()

        prompt = self.questions[opcao]
        prompt.stylize("bold yellow")

        eventos_printable : list = self.showEventsSlip(events["BetSlip"]['Bets'])
        
        if events["BetSlip"]['MultipliedOdd'] == 1:
            odd_final = 0
        else:
            odd_final = events["BetSlip"]['MultipliedOdd']

        layout.split_column(
            Layout(" ", name="empty space"),
            Layout(name="header", ratio=3),
            Layout(Panel(eventos_printable, title='[red]Boletim'), name="events", ratio=8),
            Layout(Align("[bold yellow] ODD FINAL:[/bold yellow] " + str(odd_final), align='center')),
            Layout(Align(prompt, align='center'), name="menu", ratio=3)
        )

        self.login_layout(loggedIn, layout)

        self.console.print(layout)

        return self.console.input("->")
    
    def make_filtros(self, filtros: list, filtros_ativos : list): 
        filtros_printable = []

        for index,filtro in enumerate(filtros):        
            if filtro in filtros_ativos:
                filtros_printable.append(Panel(Align(f"[bold green]{filtro}[/bold green]", align='center'), title=f'[red]{index}[/red]'))
            else:
                filtros_printable.append(Panel(Align(f"[red]{filtro}[/red]", align='center'), title=f'[red]{index}[/red]'))

        
        filtros_printable_list = Columns(filtros_printable, equal=False, expand=True)

        return filtros_printable_list
    
    
    def pergunta_filtros(self, loggedIn, filtros : list, filtros_ativos : list, currencies : list, events : list, paginas):
        self.console.clear()

        layout : Layout = Layout()

        eventos_printable : list = self.showEvents(events)

        filtros_printable_list : list = self.make_filtros(filtros, filtros_ativos)


        layout.split_column(
            Layout(" ", name="empty space"),
            Layout(name="header", ratio=3),
            Layout(Panel(eventos_printable, title=f'[red]Eventos[/red] - [bold yellow]Página {paginas[0]+1}/{paginas[1]}'), name="events", ratio=9),
            Layout(Panel(filtros_printable_list, title='[red]Filtros'), name="filters", ratio=3)
        )

        self.login_layout(loggedIn, layout)

        self.console.print(layout)

        return self.console.input("Alterar filtro: ")


    def showMenu(self, loggedIn : bool, wallet : dict[str,int], events : list, paginas, notificacoes = None):
        self.console.clear()
        layout : Layout = Layout()
        
        if not loggedIn:
            menu = [Panel("[red]E[/red]fetuar registo"), Panel("[red]F[/red]azer Login"), 
            Panel("[red]I[/red]ntroduzir Aposta"), Panel("[red]R[/red]emover Aposta"), 
            Panel("[red]C[/red]ancelar Boletim"), Panel("[red]M[/red]ostrar Boletim"), 
            Panel("[red]V[/red]alidar Boletim"), Panel("Página [red]A[/red]nterior"), 
            Panel("[red]P[/red]róxima Página"), Panel("Fil[red]t[/red]rar Eventos"), Panel("[red]S[/red]air")]
        else: 
            menu = [Panel("[red]I[/red]ntroduzir Aposta"), Panel("[red]R[/red]emover Aposta"), 
            Panel("[red]C[/red]ancelar Boletim"), Panel("[red]M[/red]ostrar Boletim"), 
            Panel("[red]V[/red]alidar Boletim"), Panel("[red]D[/red]epositar Dinheiro"), 
            Panel("[red]L[/red]evantar Dinheiro"), Panel("Página [red]A[/red]nterior"), 
            Panel("[red]P[/red]róxima Página"), Panel("Consultar [red]H[/red]istórico"), 
            Panel("Co[red]n[/red]verter Moeda"), Panel("Fil[red]t[/red]rar Eventos"), Panel("[red]S[/red]air")]

        menu_printable = Columns(menu, equal=True, expand=True)

        eventos_printable : list = self.showEvents(events)
        
        
        layout.split_column(
            Layout(" ", name="empty space"),
            Layout(name="header", ratio=3),
            Layout(Panel(eventos_printable, title=f'[red]Eventos[/red] - [bold yellow]Página {paginas[0]+1}/{paginas[1]}'), name="events", ratio=9),
            Layout(Panel(menu_printable, title='[red]Menu'), name="menu", ratio=3)
        )

        self.login_layout(loggedIn, layout, notificacoes)

        self.console.print(layout)

        return self.console.input("Introduza a letra da opção desejada -> ")


    def conclude_betslip(self, loggedIn, events):
        self.console.clear()

        if loggedIn:
            layout : Layout = Layout()

            prompt = Text("""
     _   _       _ _     _             ______       _      _   _          ___    _____    ___   _ 
    | | | |     | (_)   | |            | ___ \     | |    | | (_)        |__ \  /  ___|  / / \ | |
    | | | | __ _| |_  __| | __ _ _ __  | |_/ / ___ | | ___| |_ _ _ __ ___   ) | \ `--.  / /|  \| |
    | | | |/ _` | | |/ _` |/ _` | '__| | ___ \/ _ \| |/ _ \ __| | '_ ` _ \ / /   `--. \/ / | . ` |
    \ \_/ / (_| | | | (_| | (_| | |    | |_/ / (_) | |  __/ |_| | | | | | |_|   /\__/ / /  | |\  |
     \___/ \__,_|_|_|\__,_|\__,_|_|    \____/ \___/|_|\___|\__|_|_| |_| |_(_)   \____/_/   \_| \_/
                                                                                                
                                                                                                
    """)
            prompt.stylize("bold yellow")

            eventos_printable : list = self.showEventsSlip(events["BetSlip"]['Bets'])
            
            layout.split_column(
                Layout(" ", name="empty space"),
                Layout(name="header", ratio=3),
                Layout(Panel(eventos_printable, title='[red]Boletim'), name="events", ratio=8),
                Layout(Align("[bold yellow] ODD FINAL:[/bold yellow] " + str(events["BetSlip"]['MultipliedOdd']), align='center')),
                Layout(Align(prompt, align='center'), name="menu", ratio=3)
            )

            self.login_layout(loggedIn, layout)

            self.console.print(layout)

            resposta = self.console.input("->")

        else:
            self.invalid_info(1)
            resposta = "N"

        return resposta 

    def ask_amount(self, loggedIn, events):
        self.console.clear()

        layout : Layout = Layout()
        prompt = self.questions[3]
        prompt.stylize("bold yellow")

        eventos_printable : list = self.showEventsSlip(events["BetSlip"]['Bets'])
        
        layout.split_column(
            Layout(" ", name="empty space"),
            Layout(name="header", ratio=3),
            Layout(Panel(eventos_printable, title='[red]Boletim'), name="events", ratio=8),
            Layout(Align("[bold yellow] ODD FINAL:[/bold yellow] " + str(events["BetSlip"]['MultipliedOdd']), align='center')),
            Layout(Align(prompt, align='center'), name="menu", ratio=3)
        )

        self.login_layout(loggedIn, layout)

        self.console.print(layout)

        return self.console.input("->")
        
    def showDetailedEvent(self, loggedIn, eventos,event, paginas):
        self.console.clear()
        layout : Layout = Layout()
        participants : list = list()

        print(f'evento: {event["Sport"]["Type"]}')
        
        if event["Sport"]["Type"] == "WinDraw":
            participants.append(Panel(f"[bold yellow]{event['Intervenors'][0][0]}[/] -- {event['Intervenors'][0][1]}", title=f"[red]{0}[/red]"))
            participants.append(Panel(f"[bold yellow]{event['Intervenors'][2][0]}[/] -- {event['Intervenors'][2][1]}", title=f"[red]{1}[/red]"))
            participants.append(Panel(f"[bold yellow]{event['Intervenors'][1][0]}[/] -- {event['Intervenors'][1][1]}", title=f"[red]{2}[/red]"))
        else:
            for i,(odd,intervenor) in enumerate(event["Intervenors"]):
                participants.append(Panel(f"[bold yellow]{odd}[/] -- {intervenor}", title=f"[red]{i}[/red]"))

        participants_printable = Columns(participants, equal=True, expand=True, align='center')


        eventos_printable : list = self.showEvents(eventos)
        
        opcoes_layout : Layout = Layout()

        opcoes_layout.split_column(
            Layout(Text(event["Name"], justify='center' ), ratio=2),
            Layout(participants_printable, ratio=3)
        )

        opcoes : Layout = Layout(Panel(opcoes_layout, title=f'[red]{event["Sport"]["Name"]}[/red]'), name="menu", ratio=3)

        layout.split_column(    
            Layout(" ", name="empty space"),
            Layout(name="header", ratio=3),
            Layout(Panel(eventos_printable, title=f'[red]Eventos[/red] - [bold yellow]Página {paginas[0]+1}/{paginas[1]}'), name="events", ratio=9),
            opcoes
        )

        self.login_layout(loggedIn, layout)

        self.console.print(layout)

        return self.console.input("Introduza o número da aposta desejada -> ")

    def showEventsSlip(self, events : list):
        eventos_formatted = []
        
        for event in events:
            table_painel =  Table()
            texto = Text(str(event["EventID"]) + " | " + event["EventName"], justify='center')
            texto.stylize("red", 0, 2)
            table_painel.add_column(texto)
            
            table = Table()

            table.add_column(str("Aposta"), justify="center", style="cyan", no_wrap=True)
            table.add_column(str("Odd"), justify="center", style="bold yellow", no_wrap=True)
            
            
            table.add_row(str(event["Choice"]), str(event["Odd"]))

            table_painel.add_row(table)

            eventos_formatted.append(table_painel)
        

        return Columns(eventos_formatted, equal=False, align='center')

    def showEvents(self, events : list):
        eventos_formatted = []
        
        for event in events:
            
            table_painel = Table()
            texto = Text(str(event["Id"]) + " | " + event["Sport"]["Name"], justify='center')
            texto.stylize("bold red", 0, 2)
            table_painel.add_column(texto)

            table = Table()

            table_painel.add_row(Text(event['Name'], justify='center'))

            intervenors = [x[1] for x in event["Intervenors"]]
            odds = [str(x[0]) for x in event["Intervenors"]]
                
            if event["Sport"]["Type"] == "WinDraw":
                intervenors.remove("Draw")
                table.add_column(intervenors[0], justify="center", style="green", no_wrap=True)
                
                drawOdd = odds.pop(0)
                odds.insert(1,drawOdd)
                table.add_column("vs", justify="center", style="yellow", no_wrap=True)
                table.add_column(intervenors[1], justify="center", style="green", no_wrap=True)     
            else:
                for intervenor in intervenors:
                    table.add_column(intervenor, justify="center", style="green", no_wrap=True)  
            
            if len(odds) == 3:
                table.add_row(Text(odds[0], justify="center"), odds[1], odds[2])
            else:
                table.add_row(Text(odds[0], justify="center"), odds[1])

            table_painel.add_row(table)

            eventos_formatted.append(table_painel)
       
        return Columns(eventos_formatted, equal=False, expand=True, align='center')