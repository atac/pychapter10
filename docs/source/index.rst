
PyChapter10
===========

PyChapter10 is an open source pure Python library for reading and writing `IRIG
106 Chapter 10 (now 11)`_ files.

.. toctree::
    :maxdepth: 1

    api/index
    samples/index


Library Overview
================

Basic Structure & Usage
-----------------------

PyChapter10 makes every effort to provide a pythonic interface to Chapter 10
data as in the following example::

    for packet in C10('file.c10'):
        for message in packet:
            print(message.rtc)

The top-level C10 object represents a given Chapter 10 file or stream and can
be initialized from file or filename (default) or from bytes/string using the
from_string method. C10 objects contain Packet objects of various data types
(see API reference above). Packets attributes containing parsed/generated packet
information and generally consist of a number of messages which can be iterated
over and modified in turn.

All of these types and classes respond to the usual python introspection
resources such as help() and dir().

Modifying Data
--------------

Calling bytes() on a packet will compile the packet header, CSDW
(channel specific data word), and body (including messages) to raw bytes. You
can modify packets and messages before dumping to bytes and those changes will
be reflected in the resulting bytes object. For example::

    for msg in ethernet_packet:
        msg.ethernet_speed = 3

    out_file.write(bytes(ethernet_packet))

Generating Data from Scratch
----------------------------

You can also generate your own data. By creating a packet object of the
intended type and passing header values (or even CSDW and data) as keyword
arguments::

    messages = ...
    p = EthernetF0(count=10)
    for message in messages:
        p.append(EthernetF0.Message(data=message, length=len(message)))

Defining Data Types
-------------------

Data formats are specified using a wrapper around bitstruct_. Every data type
has a channel specific data word (CSDW) that may look something like this
(Ethernet given as an example)::

    class EthernetF0(packet.Packet):
        # ...

        csdw_format = BitFormat('''
            u16 count
            p9
            u3 ttb
            u4 format''')

Similar to a C struct fields are specified with a type (uint by default) and
bit length. "p" signifies padding or "reserved" as the chapter 10 standard
may call it. Various data types will also specify the format of the messages
they contain be that 1553, ethernet, etc. Going back to the Ethernet 
example::

    class EthernetF0(packet.Packet):
        # ...

        class Message(packet.Message):
            # ...

            def __repr__(self):
                return '<Ethernet frame %s bytes>' % len(self.data)

            FORMAT = BitFormat('''
                u64 ipts
                u14 length
                u1 data_length_error
                u1 data_crc_error
                u8 network_id
                u1 crc_error
                u1 frame_error
                u2 content
                u4 ethernet_speed''')

Now we have the intra-packet/message header defined and since it includes a
"length" field the appropriate number of bytes are read each time we get a new
message. We also define a "\__repr\__" function to help with debugging.

Contributing
============

Feedback, issues, and pull requests are all welcome on the `main repo`_. See
the CONTRIBUTING document in github for more details. If you're not sure where
to get started check out the issue tracker on github.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _IRIG 106 Chapter 10 (now 11): https://www.wsmr.army.mil/RCCsite/Documents/106-20_Telemetry_Standards/chapter11.pdf
.. _bitstruct: https://bitstruct.readthedocs.io/en/latest/
.. _main repo: https://github.com/atac/pychapter10
