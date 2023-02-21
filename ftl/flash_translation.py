from .buffer.data_cache_manage import DataCacheManage
from .physical.nand_controller import NandController, BlockType
from .address.address_translation import AddressTranslation
from .gc.garbage_collection import GarbageCollection
from dotenv import load_dotenv
import os
load_dotenv()
PHYSICAL_PAGE_SIZE_RATIO = int(os.getenv('PHYSICAL_PAGE_SIZE_RATIO'))
import random

class FlashTranslation:
    def __init__(self):
        self._dataCacheManage = DataCacheManage()
        self._nandController = NandController(self)
        self._addressTranslation = AddressTranslation()
        self._garbageCollection = GarbageCollection()
        self._garbageCollection.SetNandController(self._nandController)
        self._garbageCollection.SetAddressTranslation(self._addressTranslation)
    
    def GetBlockType(self):
        #return random.choice([BlockType.HOT, BlockType.COLD])
        return BlockType.HOT
    # return actual write bytes
    def Write(self, request):
        #print(request)
        totalWriteBytes = 0
        self._dataCacheManage.WriteCache(request)
        while True:
            page = self._dataCacheManage.GetCache()
        #    print(page)
            if not page: break 
            physicalPageAddress, writeBytes = self._nandController.Program(PHYSICAL_PAGE_SIZE_RATIO, self.GetBlockType())
            duplicateAddress = self._addressTranslation.Update(page, physicalPageAddress) 
            if duplicateAddress: self._nandController.Override(duplicateAddress)
            totalWriteBytes += writeBytes
        writeBytes = self._garbageCollection.AutoCheck(self._nandController.GetFreeSpaceRatio())
        totalWriteBytes += writeBytes
        return totalWriteBytes