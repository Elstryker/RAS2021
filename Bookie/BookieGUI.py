def showMenu():
    print(
"""
0 -> Quit
1 -> Add Event
2 -> Add Sport
3 -> Add Intervenor
4 -> Start Event
5 -> Conclude Event""")

def askParam(param):
    print(f"{param}: ")

def askLimitedParam(paramName,param,chooseMultiple = False):
    if chooseMultiple:
        print(f"{paramName} (format: option1,option2,...):")
    else:
        print(f"{paramName}:")
    for i,el in enumerate(param):
        print(f"{i+1} - {el}")

