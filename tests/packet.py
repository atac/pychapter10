from chapter10 import Packet
import unittest,os

class TestPacket(unittest.TestCase):
    def testConstruct(self):
        packet = Packet(open('samples/MSN001R1.ch10','rb'))

if __name__=='__main__':
    unittest.main()