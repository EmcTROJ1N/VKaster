from abc import ABC, abstractmethod
import json
import os

class SerializableCollection(ABC):
    Collections = dict()
    
    @staticmethod
    def GetSubClasses() -> dict:
        subClasses = dict()
        for className, value in globals().items():
            if isinstance(value, type) and issubclass(value, SerializableCollection):
                subClasses[className] = value
        return subClasses

    def __init__(self, name: str, filename: str = None, parent = None) -> None:
        if filename == None and (parent == None or name == None):
            raise Exception("A serializable collection cannot be initialized without a dump file or parent contanier and name")
        self.Parent = parent
        self.FileName = filename
        self.Name = name
        SerializableCollection.Collections[name] = self
        if filename != None and os.path.exists(filename):
            with open(filename, "r") as file:
                self.LoadCollectionFromJSON(json.load(file))

    def LoadCollectionFromJSON(self, jsonData) -> None:
        self.FileName = jsonData["FileName"]
        self.Parent = jsonData["Parent"]
        self.Name = jsonData["Name"]
        
    @abstractmethod
    def ToJSON(self) -> dict:
        return {
            "Parent": self.Parent.Name if self.Parent != None else None,
            "FileName": self.FileName,
            "Name": self.Name,
            "__collectionName__": type(self).__name__
        }

    def updateDump(self):
        if self.FileName != None:
            with open(self.FileName, "w") as file:
                json.dump(self.ToJSON(), file,
                          default=lambda o: o.__dict__, 
                          sort_keys = True, indent = 4)
        if self.Parent != None:
            self.Parent.updateDump()