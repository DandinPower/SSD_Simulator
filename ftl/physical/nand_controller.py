from libs.logs import PrintLog
from collections import deque
from tqdm import tqdm
import enum
from dotenv import load_dotenv
import os
load_dotenv()

PHYSICAL_PAGE_NUM_IN_BLOCK = int(os.getenv('PHYSICAL_PAGE_NUM_IN_BLOCK'))
PHYSICAL_BLOCK_NUM = int(os.getenv('PHYSICAL_BLOCK_NUM'))
PHYSICAL_PAGE_SIZE_RATIO = int(os.getenv('PHYSICAL_PAGE_SIZE_RATIO'))
LBA_BYTES = int(os.getenv('LBA_BYTES'))

class PageStatus(enum.Enum):
    FREE = 1
    VALID = 2
    INVALID = 3

class PhysicalBlock:
    def __init__(self, blockIdx, parentObject):
        self._parentObject = parentObject
        self._blockIdx = blockIdx
        self._pages = [PhysicalPage(self._blockIdx * PHYSICAL_PAGE_NUM_IN_BLOCK + i, self) for i in range(PHYSICAL_PAGE_NUM_IN_BLOCK)]
        self._invalid = 0
        self._currentPageIndex = 0

    def IsFull(self):
        return self._currentPageIndex == PHYSICAL_PAGE_NUM_IN_BLOCK

    def Program(self, count):
        if self._currentPageIndex == PHYSICAL_PAGE_NUM_IN_BLOCK: 
            print(f'error on : {self._blockIdx}, currentPage: {self._currentPageIndex}')
            print(f'Free block: {self._parentObject._freeBlockIndexes}')
            raise MemoryError('insufficent space to program')
        if self._pages[self._currentPageIndex]._status != PageStatus.FREE: raise MemoryError('program on not free page')
        self._pages[self._currentPageIndex]._status = PageStatus.VALID
        self._pages[self._currentPageIndex].Program(count)
        physicalPageAddress = self._pages[self._currentPageIndex]._pageAddress
        self._currentPageIndex += 1
        return physicalPageAddress
    
    def PageIsFull(self):
        self._invalid += 1

    def Erase(self):
        self._invalid = 0
        self._currentPageIndex = 0
        for page in self._pages:
            
            page.Erase()

    def __getitem__(self, index):
        return self._pages[index]
    
    def __repr__(self):
        return f'Block: {self._blockIdx} Invalid: {self._invalid} Current: {self._currentPageIndex}'
    
    def __lt__(self, other):
        return self._invalid < other._invalid

class PhysicalPage:
    def __init__(self, pageAddress, parentObject):
        self._parentObject = parentObject
        self._pageAddress = pageAddress 
        self._status = PageStatus.FREE
        self._validNum = -1

    def Program(self, count):
        self._validNum = count

    def Override(self):
        if self._status == PageStatus.INVALID: raise MemoryError('exceeds limitation')
        self._validNum -= 1
        if self._validNum == 0: 
            self._status = PageStatus.INVALID
            self._parentObject.PageIsFull()
    
    # can only access by block
    def Erase(self):
        self._status = PageStatus.FREE
        self._validNum = -1
 
    def __repr__(self):
        return f'{self._pageAddress}, {self._validNum}, status: {self._status}'
            
class NandController:
    def __init__(self, parentObject):
        self._parentObject = parentObject
        self._blocks = []
        self._freeBlockIndexes = deque([i for i in range(PHYSICAL_BLOCK_NUM)]) #寫滿pop掉, gc後append
        self._currentBlockIndex = self._freeBlockIndexes[0]
        self.InitializeBlocks()

    def AddFreeBlock(self, blockIdx):
        self._freeBlockIndexes.append(blockIdx)
    
    def EraseBlock(self, blockIdx):
        self._blocks[blockIdx].Erase()

    def RemoveFromFreeBlockIfAlreadyFree(self, blockIdx):
        if self._blocks[blockIdx].IsFull() and blockIdx in self._freeBlockIndexes:
            print(self._freeBlockIndexes)
        if not self._blocks[blockIdx].IsFull():
            self._freeBlockIndexes.remove(blockIdx)

    def InitializeBlocks(self):
        PrintLog('Build Virtual Blocks...')
        for i in tqdm(range(PHYSICAL_BLOCK_NUM)):
            self._blocks.append(PhysicalBlock(i, self))
        
    def Program(self, count):
        physicalPageAddress = self._blocks[self._currentBlockIndex].Program(count)
        if self._blocks[self._currentBlockIndex].IsFull(): 
            self._freeBlockIndexes.remove(self._currentBlockIndex)
            if len(self._freeBlockIndexes) == 0:
                print(self._blocks)
                print(self._parentObject._garbageCollection._count)
                raise IndexError('no free block')
            self._currentBlockIndex = self._freeBlockIndexes[0]
        return physicalPageAddress, PHYSICAL_PAGE_SIZE_RATIO * LBA_BYTES

    def GetHighestInvalidsBlockIdx(self):
        tempBlocks = sorted(self._blocks, reverse= True)
        return tempBlocks[0]._blockIdx

    def GetFreeSpaceRatio(self):
        return len(self._freeBlockIndexes) / PHYSICAL_BLOCK_NUM
    
    def Override(self, duplicateAddress):
        for address in duplicateAddress:
            blockIdx = address // PHYSICAL_PAGE_NUM_IN_BLOCK
            pageIdx = address % PHYSICAL_PAGE_NUM_IN_BLOCK
            self._blocks[blockIdx][pageIdx].Override()