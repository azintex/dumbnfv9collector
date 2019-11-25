from struct import unpack_from, iter_unpack
from socket import socket, AF_INET, SOCK_DGRAM
from time import time

from _es import addFlow, _esco
from create_es_index import settings
from config import clr, es

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind((clr['ip_address'], clr['port']))

# Check for capture duration. In case is 0, capture until interrupted.
if clr['dur'] != 0:
    cd = clr['dur']

def startCapture(mode='unpacked'):
    try:
        if not cd:
            while True:
                data = sock.recv(4096)
                # First unpack from bytes FlowSet header, FlowSet ID and FlowSet length.
                fsHFL = unpack_from('!HHLLLLHH', data)
                # `addFlow` function insert NetFlow v9 header data in Elasticsearch.
                addFlow(es['index']['name'], {"version": fsHFL[0], "count": fsHFL[1], \
                                                "sysUptime": fsHFL[2], "unixSeconds": fsHFL[3], \
                                                    "packageSequence": fsHFL[4], "sourceId": fsHFL[5]})
                # Check for FlowSet ID. Data record FlowSet ID greater than 255. 
                # Template record FlowSet ID in 0-255 range.
                if fsHFL[6] != 0:
                # First get unpacked iterable. 
                # The buffer’s size in bytes must be a multiple of the size required by the format (c)
                    fs = iter_unpack('!LLBHHLLLL', data[24:fsHFL[1] * clr['ts'] + 24])
                    for flow in fs:
                        addFlow(es['index']['name'], {"ipv4SourceAddress": flow[0], \
                                                        "ipv4DestinationAddress": flow[1], \
                                                            "ipProtocol": flow[2], \
                                                                "transportSourcePort": flow[3], \
                                                                    "transportDestinationPort": flow[4], \
                                                                        "counterBytes": flow[5], \
                                                                            "counterPackets": flow[6], \
                                                                                "timestampSysUptimeFirst": flow[7], \
                                                                                    "timestampSysUptimeLast": flow[8]})
    except Exception as ex:
        print(str(ex))
    finally:
        while time() < cd:
            data = sock.recv(4096)
            # First unpack from bytes FlowSet header, FlowSet ID and FlowSet length.
            fsHFL = unpack_from('!HHLLLLHH', data)
            # `addFlow` function insert NetFlow v9 header data in Elasticsearch.
            addFlow(es['index']['name'], {"version": fsHFL[0], "count": fsHFL[1], \
                                            "sysUptime": fsHFL[2], "unixSeconds": fsHFL[3], \
                                                "packageSequence": fsHFL[4], "sourceId": fsHFL[5]})
            # Check for FlowSet ID. Data record FlowSet ID greater than 255. 
            # Template record FlowSet ID in 0-255 range.
            if fsHFL[6] != 0:
            # First get unpacked iterable object. 
            # The buffer’s size in bytes must be a multiple of the size required by the format (c)
                fs = iter_unpack('!LLBHHLLLL', data[24:fsHFL[1] * clr['ts'] + 24])
                for flow in fs:
                    addFlow(es['index']['name'], {"ipv4SourceAddress": flow[0], \
                                                    "ipv4DestinationAddress": flow[1], \
                                                        "ipProtocol": flow[2], \
                                                            "transportSourcePort": flow[3], \
                                                                "transportDestinationPort": flow[4], \
                                                                    "counterBytes": flow[5], \
                                                                        "counterPackets": flow[6], \
                                                                            "timestampSysUptimeFirst": flow[7], \
                                                                                "timestampSysUptimeLast": flow[8]})
if __name__ == "__main__":
    startCapture(clr['mode'])