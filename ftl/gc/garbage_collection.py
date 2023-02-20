from ..physical.nand_controller import PageStatus
from dotenv import load_dotenv
import os
load_dotenv()

AUTO_GC_RATIO = float(os.getenv('AUTO_GC_RATIO'))

class GarbageCollection:
    def __init__(self):
        self._count = 0
        self._nandController = None

    def SetNandController(self, nandController):
        self._nandController = nandController

    def SetAddressTranslation(self, addressTranslation):
        self._addressTranslation = addressTranslation

    # use in passive gc, it will only run when free space is less than setting free ratio
    def AutoCheck(self, ratio):
        if ratio < (1 - AUTO_GC_RATIO): 
            return self.Run()
        else:
            return 0

    # implement gc because of free space is less than setting ratio
    def Run(self):
        self._count += 1
        totalWriteBytes = 0
        # find the highest invalid num block to gc
        blockIdx = self._nandController.GetHighestInvalidsBlockIdx()
        reverseMap = self._addressTranslation.GetTempReverseMap()
        # get all valid page (future all valid lba) in blockIdx
        pages = self._nandController._blocks[blockIdx]._pages
        logicalPages = []
        for page in pages: 
            if page._status == PageStatus.VALID:
                logicalPage = reverseMap[page._pageAddress]
                # program all page in to nandcontroller
                if (page._pageAddress == 114466):
                    print(logicalPage)
                logicalPages.append(logicalPage)
        for page in logicalPages:
            physicalPageAddress, writeBytes = self._nandController.Program()
            # update lba map inside page
            duplicate = self._addressTranslation.Update(logicalPage, physicalPageAddress)
            #if (114466 in duplicate):
            #    print(duplicate)
            totalWriteBytes += writeBytes
        self._nandController.RemoveFromFreeBlockIfAlreadyFree(blockIdx)
        self._nandController.AddFreeBlock(blockIdx)
        self._nandController.EraseBlock(blockIdx)
        return totalWriteBytes