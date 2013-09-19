import unittest
from chapter10.datatypes.base import Base
from chapter10 import Packet

class TestBase(unittest.TestCase):
    def setUp(self):
        self.file = open('samples/MSN001R1.ch10','rb')
        pack = Packet(self.file)
        self.data = Base(pack)

    def testParse(self):
        data = self.data.data

    def tearDown(self):
        self.file.close()

if __name__=='__main__':
    unittest.main()
