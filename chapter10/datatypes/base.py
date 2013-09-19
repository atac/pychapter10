class Base(object):
    '''
    Base object for packet data. Reads out raw bytes and stores in an attribute.
    '''

    # the names of any data attributes for lazy-loading
    dataAttrs = (
        'data',
    )

    def __init__(self,packet,noSkip=False):
        '''
        Logs the file cursor location for later and then skips past the data.
        '''

        # initialize the superclass
        object.__init__(self)

        # keep a reference to the packet object
        self.packet = packet

        # tracks whether data has been loaded
        self.init = False

        # store the file cursor position for the start of the body
        self.start = self.packet.file.tell()

        if not noSkip:
            # skip past the data for now
            packet.file.seek(self.packet.dataLength,1)

    def __load(self):
        '''
        _internal_

        Moves the file cursor around and calls the customizable parse method to load data.
        '''

        # the cursor location at the time of data retrieval
        oldPos = self.packet.file.tell()

        # skip back to the packet body
        self.packet.file.seek(self.start)

        # run the customizable reader method
        self.parse()

        # return to the original cursor position
        self.packet.file.seek(oldPos)

        # log that we've actually parsed data
        self.init = True

    def parse(self):
        '''
        Called lazily (only when requested) to avoid memory overflows.
        '''

        self.data = self.packet.file.read(self.packet.dataLength)

    def __getattribute__(self,name):
        '''
        Loads packet data on demand.
        '''

        if name != 'dataAttrs' and name in self.dataAttrs and not self.init:
            self.__load()
        return object.__getattribute__(self,name)
