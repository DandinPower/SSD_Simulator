from .write_buffer import WriteBuffer
from dotenv import load_dotenv
import os
load_dotenv()

LBA_BYTES = int(os.getenv('LBA_BYTES'))

class DataCacheManage:
    def __init__(self):
        self._writeBuffer = WriteBuffer()

    def WriteCache(self, request):
        lbaNums = request.bytes // LBA_BYTES
        if request.bytes % LBA_BYTES != 0: lbaNums += 1
        for i in range(lbaNums): self._writeBuffer.AddLba(request.lba + i)
            
    def GetCache(self):
        return self._writeBuffer.GetPage()