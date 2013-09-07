'''
Just reads each packet one at a time.
'''

from chapter10 import Packet
import sys

if __name__=='__main__':
    f = open(sys.argv[1],'rb')
    ok = 0
    try:
        while True:
            try:
                pkt = Packet(f)
                if pkt.check():
                    ok += 1
                else:
                    print pkt.check(),ok
                    print 'ERROR at packet %s' % (ok+1)
                    pkt.printHeader()
                    break
            except EOFError:
                break
    finally:
        f.close()