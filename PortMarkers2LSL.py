#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PortMarkers2LSL 0.2.1

Copyright 2017, 2019 Laurens R Krol

    Team PhyPA, Biological Psychology and Neuroergonomics,
    Technische Universitaet Berlin

    lrkrol.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
Listens for data at specified port and forwards any incoming data to an
LSL marker stream.
           
Usage:
Make sure to have pylsl installed; execute 'pip install pylsl' or see:
https://github.com/labstreaminglayer/liblsl-Python

Run PortMarkers2LSL.py and enter the requested protocol, port, et cetera.
Alternatively, run PortMarkers2LSL.py with additional arguments:

--protocol:  should be either udp or tcp.
--port:      the port to be used, 0 - 65535
--address:   address of the host
--bufsize:   size of the socket buffer (optional; default 16)
--printdata: whether or not to also print incoming data to the console
             (as boolean 0 or 1; optional; default 1)

For example:

    python .\PortMarkers2LSL.py --protocol udp --port 5005 --address 127.0.0.1

starts a marker stream relaying data coming through UDP at 127.0.0.1,
port 5005, with default buffer size of 16 and output to the console.

Note that bufsize is optional but important: if the size of the message sent 
to the socket is larger than the buffer, an error will be produced, the data
will be rejected, and an 'ERROR' marker will be sent instead.
"""

"""
2019-02-26 0.2.1 lrk
- Caught socket recv exceptions
- Made recv call non-blocking
- Made bufsize and printdata optional
2017-11-23 0.1.0 First version
"""


import pylsl
import random
import select
import socket
import string
import sys


def main(protocol, address, port, bufsize, printdata, sockettimeout):
        
    # opening socket
    sys.stdout.write('\nOpening socket... ')
    if protocol == 'udp':
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((address, port))
    elif protocol == 'tcp':
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((address, port))
        except socket.error, msg:
            print "Socket error:\n%s" % msg
            sys.exit()    

    # opening stream outlet
    sys.stdout.write('Opening stream outlet... ')
    streamname = protocol.upper() + ' Marker Stream ' + address + ':' + str(port)
    randomid = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    info = pylsl.StreamInfo(streamname, 'Markers', 1, 0, 'string', randomid)
    outlet = pylsl.StreamOutlet(info)
    print 'Done.'

    msg = 'Relaying data from ' + protocol.upper() + ' port ' + str(port) + ' on ' + address
    print '+-' + ''.join(['-' for _ in msg]) + '-+'
    print '|', msg, '|'
    print '+-' + ''.join(['-' for _ in msg]) + '-+'

    try:
        print 'Waiting for data...'
        while True:
            # waiting for data
            ready = select.select([sock], [], [], sockettimeout)
            if ready[0]:
                try:
                    if protocol == 'tcp':
                        data = sock.recv(bufsize)
                    elif protocol == 'udp':
                        data, addr = sock.recvfrom(bufsize)    
                except socket.error, msg:
                    print 'Socket error: %s' % msg
                    data = 'ERROR'
                
                # sending marker
                if data:
                    outlet.push_sample([data])
                    if printdata: print data
    except KeyboardInterrupt:
        print 'Interrupted'
            
            
if __name__ == "__main__":
    # defaults
    bufsize = 16
    printdata = 1
    sockettimeout = 5

    # setting protocol
    if('--protocol' in sys.argv):
        protocol = sys.argv[sys.argv.index('--protocol') + 1].lower()
    else:
        print '\nProtocol:\n\n  [1] TCP\n  [2] UDP\n'
        protocol = raw_input('> ')
        if protocol == '1': protocol = 'tcp'
        elif protocol == '2': protocol = 'udp'
        
    if not (protocol == 'tcp' or protocol == 'udp'):
        print 'Invalid protocol indicated'
        exit()
        
    # setting port
    if('--port' in sys.argv):
        port = int(sys.argv[sys.argv.index('--port') + 1])
    else:
        print '\nPort:\n'
        port = int(raw_input('> '))
        
    if not (port >= 0 and port <= 65535):
        print 'Invalid port indicated'
        exit()
        
    # setting address
    if('--address' in sys.argv):
        address = sys.argv[sys.argv.index('--address') + 1]
    else:
        print '\nAddress:\n'
        address = raw_input('> ')

    # requesting optional info only if nothing has been preset
    
    # setting buffer length
    if('--bufsize' in sys.argv):
        bufsize = int(sys.argv[sys.argv.index('--bufsize') + 1])
    elif len(sys.argv) == 1:
        print '\nBuffer length (default 16):\n'
        bufsize = int(raw_input('> ') or bufsize)
        
    # setting print option
    if('--printdata' in sys.argv):
        printdata = int(sys.argv[sys.argv.index('--bufsize') + 1])
    elif len(sys.argv) == 1:
        print '\n  [0] Do not print incoming data\n  [1] Print incoming data (default)\n'
        printdata = int(raw_input('> ') or printdata)
        
    main(protocol, address, port, bufsize, printdata, sockettimeout)
