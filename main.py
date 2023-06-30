from Menu import Menu
from funcs import *
from colorama import Fore, Style, init
from importlib import import_module
import Scripts
from SerializableCollections import *

authData = loadEnv()
session = None
vk = None
BlackListFileName = "BlackList.json"

if __name__ == "__main__":
    init()
    
    print(Fore.GREEN + "Loading auth data from .env file..." + Style.RESET_ALL)
    if None in [authData["LOGIN"], authData["PASSWORD"]] and authData["TOKEN"] == None:
        print(Fore.YELLOW + "Failed to load auth data from environment" + Style.RESET_ALL)
        authData = getAuthData()
    while True:
        session = dataCheck(authData)
        if session != None:
            break
        print(Fore.RED + "Failed to auth. Check auth data" + Style.RESET_ALL)
        authData = getAuthData()
    
    print(Fore.GREEN + "Auth complete!" + Style.RESET_ALL)
    vk = session.get_api()

    MenuItems = [
        Scripts.MessageBroadCast(BlackListFileName, vk),
        Scripts.EternalOnline(vk),
    ]

    VKasterMenu = Menu(MenuItems, Fore.BLUE, Fore.WHITE)
    VKasterMenu.welcomePrint()
    VKasterMenu.printItems()
    VKasterMenu.selectItem()