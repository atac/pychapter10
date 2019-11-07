
Basic Structure & Usage
=======================

PyChapter10 makes every effort to provide a pythonic interface to Chapter 10
data as in the following example::

    for packet in C10('file.c10'):
        for message in packet:
            print(message.rtc)

The top-level C10 object represents a given Chapter 10 file or stream. C10
objects contain Packet objects. Packet objects read the header and associate a
datatype-specific parser with the packet record as packet.body. Packet bodies
often consist of a number of messages which can also be iterated over.

All of these types and classes respond to the usual python introspection
resources such as help() and dir().
