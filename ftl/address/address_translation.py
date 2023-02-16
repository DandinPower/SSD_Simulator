from .map import LogicalBlock2PhysicalPage

class AddressTranslation:
    def __init__(self):
        self._lb2pp = LogicalBlock2PhysicalPage()

    # based on ppa and logical page(lba_1, lba_2, ..., lba_n) to update l2p map
    # inside l2p update, it need to update original valid data to invalid, and update mapping information
    # return override 
    def Update(self, page, physicalPageAddress):
        duplicateAddress = []
        for lba in page:
            original = self._lb2pp.Update(lba, physicalPageAddress)
            if original != None: duplicateAddress.append(original)
        return duplicateAddress
    
    def GetTempReverseMap(self):
        return self._lb2pp.GetTempReverseMap()
