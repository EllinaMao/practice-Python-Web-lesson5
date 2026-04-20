from colorama import init, Fore

init(autoreset=True)

def line(name = "", color = Fore.LIGHTBLUE_EX):
    print (color + 10*"-" + name + 10*"-")