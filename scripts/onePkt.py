from chapter10 import *
f = open('samples/MSN001R1.ch10','rb')
try:
    pkt = Packet(f)
    pkt.printHeader()
    print len(pkt) - pkt.dataLength
    print pkt.dataLength
    print len(pkt)
    print f.tell()
    print pkt.sums,pkt.checksums
finally:
    f.close()