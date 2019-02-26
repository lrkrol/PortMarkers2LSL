#!/usr/bin/env python

import random
import socket
import string
import sys

from pylsl import StreamOutlet, StreamInfo

# setting protocol
if('--protocol' in sys.argv):
    protocol = sys.argv[sys.argv.index('--protocol') + 1].lower()
else:
    print '\nProtocol:\n\n  [1] TCP\n  [2] UDP\n'
    protocol = raw_input('> ')
    if protocol == '1': protocol = 'tcp'
    elif protocol == '2': protocol = 'udp'
    
if not (protocol == 'tcp' or protocol == 'udp'):
    print 'invalid protocol indicated'
    exit()
    
# setting port
if('--port' in sys.argv):
    port = int(sys.argv[sys.argv.index('--port') + 1])
else:
    print '\nPort:\n'
    port = int(raw_input('> '))
    
if not (port >= 0 and port <= 65535):
    print 'invalid port indicated'
    exit()
    
# setting address
if('--address' in sys.argv):
    address = sys.argv[sys.argv.index('--address') + 1]
else:
    print '\nAddress:\n'
    address = raw_input('> ')
    
# setting buffer length
if('--bufsize' in sys.argv):
    bufsize = int(sys.argv[sys.argv.index('--bufsize') + 1])
else:
    print '\nBuffer length (default 16):\n'
    bufsize = int(raw_input('> ') or 16)
    
# setting print option
if('--printdata' in sys.argv):
    printdata = int(sys.argv[sys.argv.index('--bufsize') + 1])
else:
    print '\n  [0] Do not print incoming data\n  [1] Print incoming data (default)\n'
    printdata = int(raw_input('> ') or 1)

# opening socket
sys.stdout.write('\nopening socket... ')
if protocol == 'udp':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((address, port))
elif protocol == 'tcp':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((address, port))
print 'done.'

# opening stream outlet
sys.stdout.write('opening stream outlet... ')
streamname = protocol.upper() + ' Marker Stream ' + address + ':' + str(port)
randomid = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
info = StreamInfo(streamname, 'Markers', 1, 0, 'string', randomid)
outlet = StreamOutlet(info)
print 'done.'

msg = 'relaying data from ' + protocol.upper() + ' port ' + str(port) + ' on ' + address
print '+-' + ''.join(['-' for _ in msg]) + '-+'
print '|', msg, '|'
print '+-' + ''.join(['-' for _ in msg]) + '-+'

print("waiting for data...")
while True:
    # waiting for data
    if protocol == 'tcp':
        data = sock.recv(bufsize)
    elif protocol == 'udp':
        data, addr = sock.recvfrom(bufsize)
        
    # sending marker
    if data:
        outlet.push_sample([data])
        if printdata: print data