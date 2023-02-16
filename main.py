from host.host_interface import HostInterface
from dotenv import load_dotenv
import os
load_dotenv()

TRACE_LENGTH = int(os.getenv('TRACE_LENGTH'))

def main():
    hostInterface = HostInterface()
    for i in range(TRACE_LENGTH):
        hostInterface.Step()
    print(hostInterface._flashTranslation._nandController._blocks)
    hostInterface._flashTranslation._garbageCollection.Run()
    print(hostInterface._flashTranslation._nandController._blocks)
    hostInterface._flashTranslation._garbageCollection.Run()
    print(hostInterface._flashTranslation._nandController._blocks)
    
if __name__ == "__main__":
    main()