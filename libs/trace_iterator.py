from .trace import Trace 
from .logs import PrintLog
from tqdm import tqdm
import pandas as pd

class TraceIterator:
    def __init__(self):
        self._traces = []
        self._idx = 0
    
    # 將trace csv load 進來
    def Load(self, path, length=-1):
        PrintLog('use pandas to read csv....')
        self._traces.clear()
        df = pd.read_csv(path, header = None, delimiter=',', lineterminator='\n')
        loadCount = 0
        if length != -1: totalCount = length
        for index, row in tqdm(df.iterrows(), total = totalCount - 1):
            loadCount += 1
            self._traces.append(Trace(row[0], row[1], row[2], row[3]))
            if loadCount == length:
                break

    def Reset(self):
        self._idx = 0

    def GetTrace(self):
        if self.idx >= len(self._traces):
            self.idx = 0
        val = self._traces[self.idx]
        self.idx += 1
        return val
    
    def GetWriteTrace(self):        
        while 1:
            trace = self.GetTrace()
            if trace.IsWrite():
                return trace

    def __len__(self):
        return len(self._traces)