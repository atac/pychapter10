import unittest,sys
sys.path.insert(0,'..')
from chapter10 import C10

class TestC10(unittest.TestCase):
    def testInit(self):
        obj = C10('samples/MSN001R1.ch10')
        
if __name__=='__main__':
    unittest.main()