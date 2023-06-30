from SerializableCollections.SerializableCollection import SerializableCollection

class SerializableList(list, SerializableCollection):
    def __init__(self, name: str = None, filename: str = None,
                 parent: SerializableCollection = None, source: list = None) -> None:
        if source != None:
            list.__init__(self, source)
        SerializableCollection.__init__(self, name, filename, parent)

    def ToJSON(self) -> dict:
        json = super().ToJSON()
        json["data"] = list()

        for item in self:
            if isinstance(item, SerializableCollection):
                item = item.ToJSON()
            json["data"].append(item)
        return json

    def LoadCollectionFromJSON(self, jsonData):
        super().LoadCollectionFromJSON(jsonData)
        subClasses = SerializableCollection.GetSubClasses()

        def buildCollection(item):
            return subClasses[item["__collectionName__"]](item["Name"], item["FileName"], 
            SerializableCollection.Collections[item["Parent"]], item["data"])

        for item in jsonData["data"]:
            if isinstance(item, dict) and item.get("__collectionName__") in subClasses[0]:
                item = buildCollection(item)
            super().append(item)

    def append(self, __element):
        super().append(__element)
        self.updateDump()

    def extend(self, __iterable) -> None:
        super().extend(__iterable)
        self.updateDump()

    def insert(self, __index, __object) -> None:
        super().insert(__index, __object)
        self.updateDump()

    def pop(self, __index):
        value = super().pop(__index)
        self.updateDump()
        return value
    
    def remove(self, __value) -> None:
        super().remove(__value)
        self.updateDump()

    def clear(self) -> None:
        self.updateDump()
        super().clear()