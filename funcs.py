from time import sleep
import os
from dotenv import load_dotenv
from colorama import Fore, Style
import vk_api
from os.path import dirname, basename, isfile, join
from glob import glob

def animatedPrint(text: str, time: float, coloramaColor: str = "", end: str="\n"):
    perSec = time / len(text)
    for symbol in text:
        print(coloramaColor + symbol, end="", flush=True)
        sleep(perSec)
    print(end=end)

def loadEnv() -> dict:
    load_dotenv()
    return {
        "TOKEN" : os.environ.get("TOKEN"),
        "LOGIN" : os.environ.get("LOGIN"),
        "PASSWORD" : os.environ.get("PASSWORD"),
    }

def getNumAtInterval(min: int, max: int) -> int:
    num = int()
    while True:
        num = int(input())
        if min <= num < max:
            break
        print(Fore.RED + "Invalid num" + Style.RESET_ALL)
    return num

def getAuthData() -> dict:
    data = dict()
    
    print("Select an authorization method: \n1) login-password \n2) token")
    selectedMethod = getNumAtInterval(1, 3)

    if selectedMethod == 1:
        print("Login: ", end="")
        data["LOGIN"] = input()
        print("Password: ", end="")
        data["PASSWORD"] = input()
    elif selectedMethod == 2:
        print("Auth token: ", end="")
        data["TOKEN"] = input()
    else:
        print(Fore.RED + "Invalid num")
    return data

def dataCheck(data: dict) -> vk_api.VkApi:
    vkSession = None
    try:
        if data.get("TOKEN") == None:
            vkSession = vk_api.VkApi(data["LOGIN"], data["PASSWORD"])
            vkSession.auth(token_only=False)
        else:
            vkSession = vk_api.VkApi(token=data["TOKEN"])
        vk = vkSession.get_api()
        vk.wall.get(count=1)
        return vkSession
    except:
        return None

def importAllFrom(path: str) -> list:
    if path[-1] in ["/", "\\"]:
        path = path[:-1]
    print("{}/{}/*.py".format(dirname(__file__), path))
    modules = glob("{}/{}/*.py".format(dirname(__file__), path))
    return [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]