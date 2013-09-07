'''
Read through a chapter 10 file and print out a list of channel IDs found in it.
'''

from optparse import OptionParser
from chapter10 import Packet

if __name__=='__main__':
    parser = OptionParser('%prog <inputfile>')
    options,args = parser.parse_args()
    if not len(args):
        parser.print_usage()

    else:
        ids = list()
        
        f = open(args[0],'rb')
        try:
            
            # mainloop
            while True:
                
                # keep reading packets until there are no more to read
                try:
                
                    packet = Packet(f)
                    if packet.channel not in ids:
                        ids.append(packet.channel)
                    
                    # remove the packet from memory
                    del packet

                except EOFError:
                    break
                
            # print out the ids
            ids.sort()
            print 'Channel IDs:'
            for id in ids:
                print '\t' + str(id)

        # ensure the source file is closed even when an error is encountered
        finally:
            f.close()