import colorama
from colorama import Fore, Style
import random





def showMeTheColor(input):
    new_s = ""
    ForeList = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]

    for letter in input:
        rando = random.choice(ForeList)
        new_s = new_s + rando + letter

    
    
    return new_s + Style.RESET_ALL

