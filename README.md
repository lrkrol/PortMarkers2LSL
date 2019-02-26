# PortMarkers2LSL
[Lab Streaming Layer](https://github.com/sccn/labstreaminglayer) app that listens for data at a specified UDP or TCP port and forwards any incoming data to an LSL marker stream.


## Usage:
Make sure to have pylsl installed; execute `pip install pylsl` or see the [liblsl-Python GitHub page](https://github.com/labstreaminglayer/liblsl-Python).

Run `PortMarkers2LSL.py` and enter the requested protocol, port, et cetera.
Alternatively, run `PortMarkers2LSL.py` with additional arguments:

`--protocol:` should be either `udp` or `tcp`.
`--port:` the port to be used, 0 - 65535.
`--address:` address of the host.
`--bufsize:` size of the socket buffer (optional; default 16).
`--printdata:` whether or not to also print incoming data to the console (as boolean 0 or 1; optional; default 1).

For example:

`python .\PortMarkers2LSL.py --protocol udp --port 5005 --address 127.0.0.1`

starts a marker stream relaying data coming through UDP at 127.0.0.1,
port 5005, with default buffer size of 16 and output to the console.