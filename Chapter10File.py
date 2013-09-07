import struct, sys
import EasyDialogs
from array import *

ch10_pkt_header = "HHIIBBBBIHH"
ch10_pkt_header_length = struct.calcsize(ch10_pkt_header)
headers = (
    'sync',
    'chan_ID',
    'pkt_len',
    'data_len',
    'hdr_ver',
    'seq_num',
    'pkt_flgs',
    'data_typ',
    'RTCLO',
    'RTCHI',
    'chksum')
FILTER=''.join([(len(repr(chr(x)))==3) and chr(x) or '.' for x in range(256)])

def toHex(s):
    lst = []
    for ch in s:
        hv = hex(ord(ch)).replace('0x', '')
        if len(hv) == 1:
            hv - '0' + hv
        lst.append(hv)

def hexdump(src, length=16):
    result=[]
    for i in xrange(0, len(src), length):
       s = src[i:i+length]
       hexa = ' '.join(["%02X"%ord(x) for x in s])
       printable = s.translate(FILTER)
       result.append("%04X   %-*s   %s\n" % (i, length*3, hexa, printable))
    return ''.join(result)

class Chapter10File(object):
    '''
    Loads data from an open file object and provides headers as attributes.
    '''

    def __init__(self,fp):
        object.__init__(self)
        self.headers = {}
        values = struct.unpack(ch10_pkt_header,pkt_header)
        for i,value in enumerate(values):
            setattr(self,headers[i],value)
            self.headers[headers[i]] = value

    def validheader(self):
        a = array ('H')
        a.fromstring(pkt_header)
        pkt_chksum = 0

        for iVal in a[:11]:
            pkt_chksum += iVal

        return pkt_chksum & 0xffff == self.chksum

if __name__=='__main__':
    # Present a standard file-open dialog
    filename = EasyDialogs.AskFileForOpen()

    INfp = open(filename,'rb')

    obj = Chapter10File(pkt_header)
    dbuff = INfp.read(obj.pkt_len - 24)

