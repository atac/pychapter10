from chapter10 import C10
import sys

def main(filename='samples/MSN001R1.ch10'):
    C10(filename).analyze()
    
if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()