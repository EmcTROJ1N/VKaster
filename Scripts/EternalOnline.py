import vk_api
from funcs import *
from time import sleep
from Scripts.BaseScript import BaseScript

class EternalOnline(BaseScript):

    def __init__(self, vk: vk_api.VkApi) -> None:
        super().__init__(vk)

    def __str__(self) -> str:
        return "Eternal online"
    def __format__(self, __format_spec: str) -> str:
        return self.__str__().__format__(__format_spec)
    
    def Preparing(self) -> dict:
        return dict()
    
    def Execute(self, data: dict):
        animatedPrint("Now your page will be constantly online as long as the script is running", 1, Fore.GREEN)
        while True:
            try:
                self.Vk.account.setOnline(voip=0)
            except Exception as ex:
                animatedPrint(str(ex.error), 1, Fore.RED)
            else:
                animatedPrint("Signal online sended successfully", 1, Fore.GREEN)
            sleep(60)