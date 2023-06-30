from funcs import *
from colorama import Fore, Style, init
import msvcrt
import os

class Menu(object):
    def __init__(self, source : list, iconColor, fontColor):
        self.ItemsSource = source
        self.IconColor = iconColor
        self.FontColor = fontColor
    
    def welcomePrint(self):

        print(self.IconColor)
        print(self.FontColor)

        print(self.IconColor + r"""

          ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒  
         ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒  """ + self.FontColor + r""" /_/\ /_/\    /___/\/__/\    /_______/\     /_____/\     /________/\ /_____/\     /_____/\     """ + self.IconColor + r"""
        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ """ + self.FontColor + r""" \:\ \\ \ \   \::.\ \\ \ \   \::: _  \ \    \::::_\/_    \__.::.__\/ \::::_\/_    \:::_ \ \     """ + self.IconColor + r"""
        ▒▒▒▒░░▒▒░░░▒▒▒░░▒▒▒▒ """ + self.FontColor + r"""  \:\ \\ \ \   \:: \/_) \ \   \::(_)  \ \    \:\/___/\      \::\ \    \:\/___/\    \:(_) ) )_   """ + self.IconColor + r"""
        ▒▒▒▒░░░▒▒░░▒░░░░▒▒▒▒ """ + self.FontColor + r"""   \:\_/.:\ \   \:. __  ( (    \:: __  \ \    \_::._\:\      \::\ \    \::___\/_    \: __ `\ \  """ + self.IconColor + r"""
        ▒▒▒▒▒░░░░░░░░░░▒▒▒▒▒ """ + self.FontColor + r"""    \ ..::/ /    \: \ )  \ \    \:.\ \  \ \     /____\:\      \::\ \    \:\____/\    \ \ `\ \ \ """ + self.IconColor + r"""
        ▒▒▒▒▒▒▒░░░░▒▒░░░░▒▒▒ """ + self.FontColor+  r"""     \___/_(      \__\/\__\/     \__\/\__\/     \_____\/       \__\/     \_____\/     \_\/ \_\/ """ + self.IconColor + r"""
        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
         ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
          ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒  
            """)  
        animatedPrint("Automate your life in VK with ease", 1, Fore.LIGHTBLUE_EX)
        print(Fore.RESET)

    def printItems(self):
        pivot = len(self.ItemsSource) // 2
        tmp = 0
        if len(self.ItemsSource) % 2 != 0:
            tmp = 1
        
        for i in range(pivot):
            left_index = str(i + 1).ljust(2)
            right_index = str(pivot + i + 1).ljust(2)
            left_item = str(self.ItemsSource[i]).ljust(25)
            right_item = ""
            if i < pivot - tmp:
                right_item = str(self.ItemsSource[pivot + i]).ljust(25)
            print("{0}{1} {2}{3}".format(left_index, left_item, right_index, right_item))
        print()
        self.selectItem()
    

    def selectItem(self):
        animatedPrint("Enter the number of the tool you need:", .5, end=" ")
        idx = getNumAtInterval(1, len(self.ItemsSource) + 1) - 1
        os.system('cls' if os.name == 'nt' else 'clear')

        data = self.ItemsSource[idx].Preparing()
        print(Fore.GREEN + "Script loaded, press key for beginning . . .\n", Style.RESET_ALL, end="")
        msvcrt.getch()
        self.ItemsSource[idx].Execute(data)