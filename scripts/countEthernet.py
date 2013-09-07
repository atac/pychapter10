import chapter10

f = open('samples/MSN001R1.ch10','rb')
obj = chapter10.C10(f)
packets = 0
for i,packet in enumerate(obj.packets):
    if isinstance(packet.body,chapter10.datatypes.Ethernet):
        packets += 1
print '%i ethernet packets found' % packets