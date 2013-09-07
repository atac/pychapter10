'''
THIS IS AN INCOMPLETE MODULE!
    use at your own risk
'''

from base import Base
import struct

class Message(Base):
    '''
    Represents a single ethernet message that can be a whole message (type complete) or
    part of a larger message (type segmented).
    '''
    
    def __init__(self,packet):
        '''
        Read out the header info for a single ethernet message.
        '''
        
        # initialize the superclass
        Base.__init__(self,packet,noSkip=True)
        
        # skip the intra-packet time header
        self.packet.file.seek(2,1)
        
        # get the length of the message
        self.length = struct.unpack('B',self.packet.file.read(1))[0]
        
        # hack to fix strange length anomaly
        if self.length in (0x92,0xb2):
            self.length += 2
            
        # the cursor position at the start of the data
        self.start = self.packet.file.tell()
        
        # flag to indicate data has been loaded
        self.init = False
        
        # skip the rest of the data header and the message body
        self.packet.file.seek(self.length,1)
        
    def full(self):
        '''
        Should return a valid string representation of the packet data (including message
        headers) suitable for writing to file.
        '''
        
        pass
        
    def parse(self):
        self.data = self.packet.file.read(self.length+3)
        
class Ethernet(Base):
    '''
    An ethernet body containing one or more Message objects.
    '''
    
    dataAttrs = (
        'messages',
    )
    
    def __init__(self,packet):
        '''
        Parse ethernet specific information.
        '''
        
        # initialize the superclass without skipping data
        Base.__init__(self,packet,noSkip=True)
        
        # read the channel specific data words
        self.messageCount,type = struct.unpack('bb',packet.file.read(2))
        
        #@todo: parse the type
        
        # skip past the actual body
        self.packet.file.seek(self.packet.dataLength-2,1)
        
    def parse(self):
        '''
        Parses ethernet messages into objects.
        '''

        self.messages = [Message(self.packet) for i in range(self.messageCount)]
        
    def __iter__(self):
        return iter(self.messages)
    
    def __len__(self):
        return len(self.messages)