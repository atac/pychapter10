'''
Extract video from a chapter 10 file.
'''

from chapter10 import *
from optparse import OptionParser,make_option
from array import array
import os

if __name__=='__main__':
    parser = OptionParser('%prog <inFile> [outDir] [options]',option_list=(
        make_option('-c','--channels',default='',
            help='a comma-seperated list of channels to take video from'),
    ))
    options,args = parser.parse_args()
    if not args:
        print 'not enough arguments!'
        parser.print_usage()
    else:
        if len(args) > 1:
            targetDir = os.path.abspath(args[1])
        else:
            targetDir = os.path.abspath(os.curdir)
        if not os.path.exists(targetDir):
            os.makedirs(targetDir)
        if options.channels:
            targetChannels = [int(x.strip()) for x in options.channels.split(',')]
        else:
            targetChannels = []
        inFile = open(args[0],'rb')
        outFiles = {}
        try:
            while True:
                try:
                    pkt = Packet(inFile)
                except EOFError:
                    break
                if targetChannels and pkt.channel in targetChannels:
                    if pkt.channel not in outFiles:
                        outFiles[pkt.channel] = open(
                            os.path.join(targetDir,str(pkt.channel))+'.mpg',
                            'wb')
                    a = array('H',pkt.body.data[4:])
                    a.byteswap()
                    # a.tofile(<file>) doesn't seem to be working :-/
                    outFiles[pkt.channel].write(a.tostring())
        finally:
            inFile.close()
            for file in outFiles.values():
                file.close()
