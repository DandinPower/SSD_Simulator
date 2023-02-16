from collections import deque
from dotenv import load_dotenv
import os
load_dotenv()

PHYSICAL_PAGE_SIZE_RATIO = int(os.getenv('PHYSICAL_PAGE_SIZE_RATIO'))

class WriteBuffer:
    def __init__(self):
        self._buffer = deque()
    
    def AddLba(self, lba):
        self._buffer.append(lba)
    
    def GetPage(self):
        if len(self._buffer) < PHYSICAL_PAGE_SIZE_RATIO:
            return None
        # return (lba_1, lba_2, ..., lba_N)
        return tuple(self._buffer.popleft() for _ in range(PHYSICAL_PAGE_SIZE_RATIO))