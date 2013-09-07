from packet import Packet
import atexit,os

class C10(object):
    '''
    A file wrapper that parses Chapter 10 packets.
    '''

    def __init__(self,file):
        '''
        Takes a file or filename and reads packets.
        '''
        
        # initialize the superclass
        object.__init__(self)
        
        # open a file if a string was given
        if type(file) == str:
            file = open(file,'rb')
            atexit.register(file.close)
        
        # save a reference to the file object
        self.file = file

        # read packets until end-of-file (EOF)
        self.packets = []
        self.size = 0
        while True:
            try:
                packet = Packet(self.file)
                self.packets.append(packet)
                self.size += len(packet)
            except EOFError:
                break
            
    def analyze(self):
        print '''File: %s
Packets: %s
Total size: %s bytes''' % (os.path.abspath(self.file.name),
                           len(self.packets),
                           self.size)

    def __len__(self):
        return len(self.packets)
    
    def __iter__(self):
        return iter(self.packets)