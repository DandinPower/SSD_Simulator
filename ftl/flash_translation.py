from .buffer.data_cache_manage import DataCacheManage
from .physical.nand_controller import NandController
from .address.address_translation import AddressTranslation
from .gc.garbage_collection import GarbageCollection

class FlashTranslation:
    def __init__(self):
        self._dataCacheManage = DataCacheManage()
        self._nandController = NandController()
        self._addressTranslation = AddressTranslation()
        self._garbageCollection = GarbageCollection()
        self._garbageCollection.SetNandController(self._nandController)
        self._garbageCollection.SetAddressTranslation(self._addressTranslation)
    # return actual write bytes
    def Write(self, request):
        totalWriteBytes = 0
        self._dataCacheManage.WriteCache(request)
        while True:
            page = self._dataCacheManage.GetCache()
            if not page: break 
            physicalPageAddress, writeBytes = self._nandController.Program()
            if (physicalPageAddress == 0):
                print(page, physicalPageAddress)
            duplicateAddress = self._addressTranslation.Update(page, physicalPageAddress) 
            if duplicateAddress: self._nandController.Override(duplicateAddress)
            totalWriteBytes += writeBytes
        writeBytes = self._garbageCollection.AutoCheck(self._nandController.GetFreeSpaceRatio())
        totalWriteBytes += writeBytes
        return totalWriteBytes