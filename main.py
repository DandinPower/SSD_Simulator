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
        history.AddHistory(i, request.bytes, writeBytes)
    history.ShowHistory('test.png')
    
if __name__ == "__main__":
    main()