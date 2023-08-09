import vk_api
from funcs import *
from Scripts.BaseScript import BaseScript

from bs4 import BeautifulSoup as BS
from selenium import webdriver
from pyvirtualdisplay import Display

class YoutubeNotifications(BaseScript):

    def __init__(self, vk: vk_api.VkApi) -> None:
        super().__init__(vk)

    def __str__(self) -> str:
        return "Youtube notifications"
    def __format__(self, __format_spec: str) -> str:
        return self.__str__().__format__(__format_spec)
    
    def Preparing(self) -> dict:
        data = dict()
        print("The script will send notifications to all subscribers in the group when a new video is released on the YouTube channel")
        
        print("Enter chrome webdriver path:", end=" ")
        data["driver"] = input()

        print("Enter youtube channel link:", end=" ")
        data["YTurl"] = input()
        return data
    
    def Execute(self, data: dict):
        animatedPrint("All subscribers subscribers will now receive notifications when a new video is released on the channel", 1, Fore.GREEN)

        while True:
            with Display():
                driver = webdriver.Chrome(data["driver"])
                driver.get(data["YTUrl"])
                sleep(10)  #Можно ждать до загрузки страницы, но проще подождать 10 секунд, их хватит с запасом
                html = driver.page_source
            
            soup = BS(html, "html.parser")
            videos = soup.find_all("ytd-grid-video-renderer",{"class":"style-scope ytd-grid-renderer"})
            a = videos[0].find("a",{"id":"video-title"})
            link = "https://www.youtube.com" + a.get("href")
            
            def updateUrl(url):
                with open("lastUrl.dat", "w") as file:
                    print(url, file=file)

            def notifySubs(url):
                members = []
                group_id = self.Vk.groups.getById()[0]["id"]
                singleRequestCount = 1000
                currentOffset = 0
                
                while True:
                    response = self.Vk.groups.getMembers(group_id=group_id, offset=currentOffset, count=singleRequestCount)
                    members.extend(response["items"])
                    if currentOffset + singleRequestCount >= response["count"]:
                        break
                    offset += singleRequestCount

                i = 0
                while i < len(members):
                    try:
                        self.Vk.messages.send(user_ids = members[i : i + 100])
                        i += 100
                    except:
                        pass

            if os.path.isfile("lastUrl.dat") == False:
                updateUrl(link)
                continue

            with open("lastUrl.dat", "r") as file:
                url = file.read()
                if url != link:
                    print('New video was uploaded')
                    updateUrl(url)
                    notifySubs(url)
            sleep(180)