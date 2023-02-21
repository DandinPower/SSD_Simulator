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

class BlockType(enum.Enum):
    NONE = 1
    HOT = 2
    COLD = 3

class PhysicalBlock:
    def __init__(self, blockIdx, parentObject):
        self._parentObject = parentObject
        self._blockIdx = blockIdx
        self._pages = [PhysicalPage(self._blockIdx * PHYSICAL_PAGE_NUM_IN_BLOCK + i, self) for i in range(PHYSICAL_PAGE_NUM_IN_BLOCK)]
        self._invalid = 0
        self._currentPageIndex = 0
        self._type = BlockType.NONE

    def IsFull(self):
        return self._currentPageIndex == PHYSICAL_PAGE_NUM_IN_BLOCK

    def Program(self, count, type):
        # 設定初始化Type
        if (self._type == BlockType.NONE):
            self._type = type
        # 檢查是否寫在正確的Block Type上 
        if self._type != type:
            raise TypeError('program on different type block')
        # Program在一個已經滿的Block上
        if self._currentPageIndex == PHYSICAL_PAGE_NUM_IN_BLOCK: 
            raise MemoryError('insufficent space to program')
        # Program在滿的Page Index上
        if self._pages[self._currentPageIndex]._status != PageStatus.FREE: 
            raise MemoryError('program on not free page')
        # 標示該Page的狀態以及紀錄寫入的LBA數量
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
        self._type = BlockType.NONE
        for page in self._pages:
            page.Erase()

    def __getitem__(self, index):
        return self._pages[index]
    
    def __repr__(self):
        return f'Block: {self._blockIdx} Invalid: {self._invalid} Current: {self._currentPageIndex} Type: {self._type}\n'
    
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
        self._currentHotBlockIndex = None 
        self._currentColdBlockIndex = None 
        self.InitializeBlocks()
        
    def EraseBlock(self, blockIdx):
        # 要把所有只到block裡page的map刪掉
        
        # RemoveFromFreeBlockIfAlreadyFree
        if not self._blocks[blockIdx].IsFull():
            self._freeBlockIndexes.remove(blockIdx)
        # AddFreeBlock
        self._freeBlockIndexes.append(blockIdx)
        self._blocks[blockIdx].Erase()

    def InitializeBlocks(self):
        PrintLog('Build Virtual Blocks...')
        for i in tqdm(range(PHYSICAL_BLOCK_NUM)):
            self._blocks.append(PhysicalBlock(i, self))
        
    # 欲取得符合該type的block index
    def GetFreeBlock(self, type):
        if (type == BlockType.HOT):
            if self._currentHotBlockIndex:
                return self._currentHotBlockIndex
            if self._currentColdBlockIndex == self._freeBlockIndexes[0]:
                if len(self._freeBlockIndexes) == 1:
                    raise IndexError('no free hot block')
                else:
                    self._currentHotBlockIndex = self._freeBlockIndexes[1]
                    return self._currentHotBlockIndex
            self._currentHotBlockIndex = self._freeBlockIndexes[0]
            return self._currentHotBlockIndex
        elif (type == BlockType.COLD):
            if self._currentColdBlockIndex:
                return self._currentColdBlockIndex
            if self._currentHotBlockIndex == self._freeBlockIndexes[0]:
                if len(self._freeBlockIndexes) == 1:
                    raise IndexError('no free cold block')
                else:
                    self._currentColdBlockIndex = self._freeBlockIndexes[1]
                    return self._currentColdBlockIndex
            self._currentColdBlockIndex = self._freeBlockIndexes[0]
            return self._currentColdBlockIndex
        else:
            raise TypeError('unknown block type')
        
    def ClearFreeBlockIndex(self, type):
        if (type == BlockType.HOT):
            self._currentHotBlockIndex = None
        elif (type == BlockType.COLD):
            self._currentColdBlockIndex = None
        else:
            raise TypeError('unknown block type')

    # count 為寫入SSD的page數量, type為寫入的Block種類 (需使用BlockType Enum)
    def Program(self, count, type):
        programBlockIndex = self.GetFreeBlock(type)
        physicalPageAddress = self._blocks[programBlockIndex].Program(count, type)
        if self._blocks[programBlockIndex].IsFull():
            self._freeBlockIndexes.remove(programBlockIndex)
            self.ClearFreeBlockIndex(type)
        if len(self._freeBlockIndexes) == 0:
            raise IndexError('no free block')
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