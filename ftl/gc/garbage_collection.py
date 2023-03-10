from ..physical.nand_controller import PageStatus
import copy
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
        blockType = self._nandController._blocks[blockIdx]._type
        reverseMap = self._addressTranslation._lb2pp._inverseMap
        pages = self._nandController._blocks[blockIdx]._pages
        logicalPages = []
        for page in pages: 
            if page._status == PageStatus.VALID:
                logicalPage = sorted(copy.deepcopy(reverseMap[page._pageAddress]))
                logicalPages.append(logicalPage)
        for page in logicalPages:
            programCount = len(page)
            physicalPageAddress, writeBytes = self._nandController.Program(programCount, blockType)
            duplicate = self._addressTranslation.Update(page, physicalPageAddress)
            totalWriteBytes += writeBytes
        self._nandController.EraseBlock(blockIdx)
        return totalWriteBytes