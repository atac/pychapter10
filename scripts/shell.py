import sys
from code import InteractiveConsole
from chapter10 import *

def main(filename='samples/MSN001R1.ch10'):
    file = C10(open(filename,'rb'))
    d = file.__dict__.copy()
    d['obj'] = file
    shell = InteractiveConsole(d,'<shell>')
    shell.interact()

if __name__=='__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
