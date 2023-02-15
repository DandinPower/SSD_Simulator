class Trace:
    def __init__(self, opCode, fid, lba, bytes):
        self._opCode = opCode 
        self._fid = fid 
        self._lba = lba 
        self._bytes = bytes
    
    def IsRead(self):
        return self._opCode == 1
    
    def IsWrite(self):
        return self._opCode == 2

    def __str__(self):
        return f'Trace: OpCode {self._opCode}, Fid {self._fid}, Lba {self._lba}, Bytes {self._bytes}'