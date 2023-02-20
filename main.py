from host.host_interface import HostInterface
from tqdm import tqdm
from dotenv import load_dotenv
import os
load_dotenv()

TRACE_LENGTH = int(os.getenv('TRACE_LENGTH'))

def main():
    hostInterface = HostInterface()
    for i in tqdm(range(TRACE_LENGTH)):
        request, writeBytes = hostInterface.Step()
        #print(request.bytes, writeBytes)
    print(f'GC Count: {hostInterface._flashTranslation._garbageCollection._count}')
if __name__ == "__main__":
    main()