import vk_api
from abc import ABC, abstractmethod

class BaseScript(ABC):
    def __init__(self, vk: vk_api.VkApi) -> None:
        self.Vk = vk

    @abstractmethod
    def Preparing(self) -> dict:
        raise Exception("Preparing method would be overrided")
    
    @abstractmethod
    def Execute(self, data: dict):
        raise Exception("Execute method would be overrided")

    def __str__(self) -> str:
        raise Exception("__str__ method would be overrided")
    def __format__(self) -> str:
        raise Exception("__format__ method would be overrided")