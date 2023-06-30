from funcs import *
from SerializableCollections import SerializableDict, SerializableList
from random import randint
from Scripts.BaseScript import BaseScript

class MessageBroadCast(BaseScript):
    __BlackList = None
    
    def __init__(self, filename, vk: vk_api.VkApi) -> None:
        super().__init__(vk)
        name = os.path.splitext(os.path.basename(filename))[0]
        self.__BlackList = SerializableDict(name=name, filename=filename)
    
    def __str__(self) -> str:
        return "Message broadcasting"
    def __format__(self, __format_spec: str) -> str:
        return self.__str__().__format__(__format_spec)

    def Preparing(self) -> dict:
        data = dict()
        print("This script performs a mass mailing of the specified message to a random sample of users in a given group")
        print("Enter target group id:", end=" ")
        data["group_id"] = input()
        print("Enter count of recipients:", end=" ")
        data["count"] = int(input())
        print("Enter message for broadcasting:", end=" ")
        data["message"] = input()
        return data
    

    def Execute(self, data: dict):
        if None in [data.get("message"), data.get("count"),
                    data.get("group_id")]:
            print(Fore.RED + "Invalid data given, aborting..." + Style.RESET_ALL)
            return

        if (self.__BlackList.get(data["group_id"]) == None):
            self.__BlackList[data["group_id"]] = SerializableList(parent= self.__BlackList, name= data["group_id"])

        def getUsersCount(group_id) -> int:
            return self.Vk.groups.getMembers(group_id = group_id)["count"]

        def generateId(count: int = None) -> int:
            users = None
            if count == None:
                count = getUsersCount(data["group_id"])
            
            if count >= 1000:
                offset = randint(0, count - 1000)
                users = self.Vk.groups.getMembers(group_id = data["group_id"],
                                             offset = offset)
            elif users == None:
                users = self.Vk.groups.getMembers(group_id = data["group_id"])
            usersIds = users["items"]

            currentId = usersIds[randint(0, len(usersIds)) - 1]
            while len(usersIds) > 0 and currentId in self.__BlackList[data["group_id"]]:
                flag = currentId in self.__BlackList[data["group_id"]]
                usersIds.remove(currentId)
                idx = randint(0, len(usersIds) - 1)
                currentId = usersIds[idx]
            
            return currentId

        sended = 0
        groupUsersCount = getUsersCount(data["group_id"])
        for i in range(data["count"]):
            try:
                if groupUsersCount - len(self.__BlackList[data["group_id"]]) < data["count"] - sended:
                    raise Exception("Not enough users in the group for broadcasting..." + Style.RESET_ALL)
                id = generateId(groupUsersCount)
                self.Vk.messages.send(user_id = id, message = data["message"],
                random_id = vk_api.utils.get_random_id())
            except vk_api.ApiError as ex:
                if ex.code in [7, 902]:
                    self.__BlackList[data["group_id"]].append(id)
                print(Fore.RED + str(ex) + Style.RESET_ALL)
            else:
                print(Fore.GREEN + "Message sended to {}...".format(id) + Style.RESET_ALL)
                sended += 1
                self.__BlackList[data["group_id"]].append(id)
        print(Fore.GREEN + "Finally sended messages: {}".format(sended) + Style.RESET_ALL)