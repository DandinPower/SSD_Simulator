from collections import defaultdict
from dotenv import load_dotenv
import os
load_dotenv()

PHYSICAL_PAGE_SIZE_RATIO = int(os.getenv('PHYSICAL_PAGE_SIZE_RATIO'))

class LogicalBlock2PhysicalPage:
    def __init__(self):
        #self._map = dict()
        self._map = dict()
        self._inverseMap = defaultdict(list)

    def Update(self, lba, physicalPageAddress):
        # update logical to physical map
        original = self._map.get(lba)
        self._map[lba] = physicalPageAddress
        if original != None:
            self._inverseMap[original].remove(lba)
        self._inverseMap[physicalPageAddress].append(lba)
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