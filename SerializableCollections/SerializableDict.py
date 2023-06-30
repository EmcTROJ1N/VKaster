from SerializableCollections.SerializableCollection import SerializableCollection
import re

class SerializableDict(dict, SerializableCollection):
    def __init__(self, name: str = None, filename: str = None, parent: SerializableCollection = None, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        SerializableCollection.__init__(self, name, filename, parent)

    def ToJSON(self) -> dict:
        json = super().ToJSON()
        json["data"] = dict()
        for key, value in self.items():
            if isinstance(key, SerializableCollection):
                key = key.ToJSON()
            if isinstance(value, SerializableCollection):
                value = value.ToJSON()
            json["data"][key] = value
        return json
    
    def LoadCollectionFromJSON(self, jsonData):
        super().LoadCollectionFromJSON(jsonData)
        subClasses = SerializableCollection.GetSubClasses()
        
        def buildCollection(item):
            return subClasses[item["__collectionName__"]](item["Name"], item["FileName"], 
            SerializableCollection.Collections[item["Parent"]], item["data"])
        
        for key, value in jsonData["data"].items():
            if re.match(r"__.*__", key):
                continue
            if isinstance(key, dict) and key.get("__collectionName__") in subClasses.keys():
                key = buildCollection(key)
            if isinstance(value, dict) and value.get("__collectionName__") in subClasses.keys():
                value = buildCollection(value)
            
            super().__setitem__(key, value)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.updateDump()
        
    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self.updateDump()
    
    def clear(self) -> None:
        super().clear()
        self.updateDump()
    
    def pop(self, key):
        super().pop(key)
        self.updateDump()

    def popitem(self):
        super().popitem()
        self.updateDump()