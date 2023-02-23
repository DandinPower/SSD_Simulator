from .map import LogicalBlock2PhysicalPage

class AddressTranslation:
    def __init__(self):
        self._lb2pp = LogicalBlock2PhysicalPage()
        
    def Update(self, page, physicalPageAddress):
        duplicateAddress = []
        for lba in page:
            original = self._lb2pp.Update(lba, physicalPageAddress)
            if original != None: 
                duplicateAddress.append(original)
        return duplicateAddress
    
    def GetTempReverseMap(self):
        return self._lb2pp.GetTempReverseMap()