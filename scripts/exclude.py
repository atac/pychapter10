'''
Copy a chapter 10 file over packet by packet while optionally excluding a
specific channel by ID.
'''

from chapter10 import *
from optparse import OptionParser
import os

def copyPacket(packet,src,dst):
    '''
    Take a packet and copy it from an input file to an output file.
    '''
    
    # remember the old file position
    oldPos = src.tell()
    
    # go to the start of the packet
    src.seek(packet.filePos)
    
    # read it out
    raw = src.read(packet.length)
    
    # then write it out
    dst.write(raw)
    
    # finally, return the source to its original position
    src.seek(oldPos)

if __name__=='__main__':
    parser = OptionParser('%prog <inFile> <outFile> [options]')
    parser.add_option('-e','--exclude',dest='exclude',default=None,type='int',
                      help='exclude a specific channel from the copy')
    parser.add_option('-f','--force',default=False,action='store_true',
                      dest='force',help='force overwrite if outFile exists')
    parser.add_option('-v','--verbosity',default=1,type='int',
                      help='set the verbosity of the script output: \
0 (silent), 1 (normal), or 2 (verbose)')
    options,args = parser.parse_args()
    
    # validate the file arguments
    if len(args) != 2:
        parser.print_usage()
        print 'not enough arguments!'

    elif not os.path.exists(args[0]):
        parser.print_usage()
        print '%s was not found!' % args[0]

    elif os.path.exists(args[1]) and not options.force:
        parser.print_usage()
        print '%s already exists, remove it or use -f to overwrite' % args[1]

    else:
        if options.verbosity > 0:
            s = 'Copying packets from %s to %s' % tuple(args)
            if options.exclude:
                s += ' excluding channel %s' % options.exclude
            print s
        
        # open our two files
        src = open(args[0],'rb')
        dst = open(args[1],'wb')
        
        try:
            
            # mainloop
            while True:
                
                try:
                    
                    # read the packet
                    packet = Packet(src)
        
                    # only copy if it's not an exclude
                    if not options.exclude or \
                            options.exclude != packet.channel:
                        if options.verbosity == 2:
                            print '\tcopying packet in channel %s...' % \
                                packet.channel,
                        copyPacket(packet,src,dst)
                        if options.verbosity == 2:
                            print 'done'

                    elif options.exclude and options.verbosity == 2:
                        print '\tdiscriminating against packet in channel %s' \
                            % options.exclude
                
                # quit the mainloop when we reach the end of the file
                except EOFError:
                    break
        
        # ensure the source and output files get closed even in case
        # of an error
        finally:
            src.close()
            dst.close()
            
        print 'Finished'