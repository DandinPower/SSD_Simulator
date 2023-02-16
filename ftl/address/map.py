class LogicalBlock2PhysicalPage:
    def __init__(self):
        self._map = dict()
    
    def Update(self, lba, physicalPageAddress):
        original = self._map.get(lba)
        self._map[lba] = physicalPageAddress
        return original

    def GetTempReverseMap(self):
        reverseMap = {}
        for key, value in self._map.items():
            if value not in reverseMap:
                reverseMap[value] = [key]
            else:
                reverseMap[value].append(key)
        return reverseMap

    def GetPhysicalPageAddress(self, lba):
        return self._map[lba]
    
    def __str__(self):
        return f'{self._map}'