from chapter10 import *
from sys import argv as args

def main(inFile='samples/MSN001R1.ch10',outFile='output.pcap'):
    out = open(outFile,'wb')
    try:
        for packet in C10(inFile):
            if isinstance(packet.body,datatypes.Ethernet):
                for message in packet.body:
                    out.write(message.full())
    finally:
        out.close()
        
if __name__=='__main__':
    args = list(args)
    args.remove(args[0])
    main(*args)