from chapter10 import *
import sys

def main(filename='samples/MSN001R1.ch10'):
    for packet in C10(filename):
        packet.printHeader()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
