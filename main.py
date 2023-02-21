from host.host_interface import HostInterface
from libs.history import WAFHistory
from tqdm import tqdm
from dotenv import load_dotenv
import os
load_dotenv()

TRACE_LENGTH = int(os.getenv('TRACE_LENGTH'))

def main():
    hostInterface = HostInterface()
    history = WAFHistory()
    for i in tqdm(range(TRACE_LENGTH)):
        request, writeBytes = hostInterface.Step()
        #print(hostInterface._flashTranslation._nandController._blocks)
        #print(hostInterface._flashTranslation._addressTranslation._lb2pp._map)
        #print(hostInterface._flashTranslation._addressTranslation._lb2pp._inverseMap)
        history.AddHistory(i, writeBytes / request.bytes)
    history.ShowHistory('test.png')
    

if __name__ == "__main__":
    main()