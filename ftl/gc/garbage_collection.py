from ..physical.nand_controller import PageStatus
from dotenv import load_dotenv
import os
load_dotenv()

AUTO_GC_RATIO = float(os.getenv('AUTO_GC_RATIO'))

class GarbageCollection:
    def __init__(self):
        self._nandController = None

    def SetNandController(self, nandController):
        self._nandController = nandController

    def SetAddressTranslation(self, addressTranslation):
        self._addressTranslation = addressTranslation

    # implement gc because of free space is less than setting ratio
    def Run(self):
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
                logicalPages.append(logicalPage)
        for page in logicalPages:
            physicalPageAddress = self._nandController.Program()
            # update lba map inside page
            self._addressTranslation.Update(logicalPage, physicalPageAddress)
        self._nandController.AddFreeBlock(blockIdx)
        self._nandController.EraseBlock(blockIdx)

    # use in passive gc, it will only run when free space is less than setting free ratio
    def AutoCheck(self, ratio):
        if ratio < (1 - AUTO_GC_RATIO): 
            self.Run()