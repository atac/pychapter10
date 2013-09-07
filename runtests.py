'''
Import and run all tests for the library.
'''

from tests import *
import unittest,sys,shutil

if __name__=='__main__':
    # allow for printing testcase names as they run
    if len(sys.argv) > 1 and sys.argv[1] == 'verbose':
        sys.argv.remove('verbose')
        verbosity = 2
    else:
        verbosity = 1

    # run the default testrunner
    unittest.main(testRunner=unittest.TextTestRunner(verbosity=verbosity))