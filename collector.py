from struct import unpack_from, iter_unpack
from socket import socket, AF_INET, SOCK_DGRAM
from time import time

# clr - Collector config options.
# es - Elasticsearch config options.
from config import clr, es

# addFlow function for add data record FlowSets in Elasticsearch.
from _es import addFlow

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind((clr['ip_address'], clr['port']))

index = es['index']['prefix'] + es['index']['name']


def getDataRecordFlowSets():
    data = sock.recv(4096)
    # First unpack from bytes FlowSet header, FlowSet ID and FlowSet length.
    fsHFL = unpack_from('!HHLLLLHH', data)
    # `addFlow` function insert NetFlow v9 header data in Elasticsearch.
    #addFlow(index, {"version": fsHFL[0], "count": fsHFL[1], \
                        #"sysUptime": fsHFL[2], "unixSeconds": fsHFL[3], \
                            #"packageSequence": fsHFL[4], "sourceId": fsHFL[5]})
    fsd = {"version": fsHFL[0], "count": fsHFL[1], \
                        "sysUptime": fsHFL[2], "unixSeconds": fsHFL[3], \
                            "packageSequence": fsHFL[4], "sourceId": fsHFL[5]}
    # Check for FlowSet ID. Data record FlowSet ID greater than 255. 
    # Template record FlowSet ID in 0-255 range.
    if fsHFL[6] != 0:
        # First get unpacked iterable. 
        # The buffer’s size in bytes must be a multiple of the size required by the format (c)
        fs = iter_unpack('!LLBHHLLLL', data[24:fsHFL[1] * clr['ts'] + 24])
        for flow in fs:
            fsd.update({"ipv4SourceAddress": flow[0], \
                                "ipv4DestinationAddress": flow[1], \
                                    "ipProtocol": flow[2], \
                                        "transportSourcePort": flow[3], \
                                            "transportDestinationPort": flow[4], \
                                                "counterBytes": flow[5], \
                                                    "counterPackets": flow[6], \
                                                        "timestampSysUptimeFirst": flow[7], \
                                                            "timestampSysUptimeLast": flow[8]})
            print(fsd)
            """ addFlow(index, fsd.update({"ipv4SourceAddress": flow[0], \
                                "ipv4DestinationAddress": flow[1], \
                                    "ipProtocol": flow[2], \
                                        "transportSourcePort": flow[3], \
                                            "transportDestinationPort": flow[4], \
                                                "counterBytes": flow[5], \
                                                    "counterPackets": flow[6], \
                                                        "timestampSysUptimeFirst": flow[7], \
                                                            "timestampSysUptimeLast": flow[8]})) """


def startCapture(mode='unpacked'):
    # Check for capture duration.
    if clr['dur'] != 0:
        cd = time() + clr['dur']
        while time() < cd:
            getDataRecordFlowSets()
    else:
        while True:
            getDataRecordFlowSets()
    
if __name__ == "__main__":
    startCapture(clr['mode'])