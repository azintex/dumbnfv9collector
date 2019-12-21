from struct import unpack_from, iter_unpack
from socket import socket, AF_INET, SOCK_DGRAM
from time import time
import io

# clr - Collector config options.
# es - Elasticsearch config options.
from config import clr, es

# addFlow function for add data record FlowSets in Elasticsearch.
#from _es import addFlow

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(('172.16.93.5', 2055))

index = es['index']['prefix'] + es['index']['name']

def getFlowSetId(flowSet):
    id = unpack_from('H', flowSet, 20)
    return id[0]

def getFlowSetHeader(flowSet):

    # 0                   1                   2                   3
    # 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    # |       Version Number          |            Count              |
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    # |                           sysUpTime                           |
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    # |                           UNIX Secs                           |
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    # |                       Sequence Number                         |
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    # |                        Source ID                              |
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

    flowSetHeader = unpack_from('!HHLLLL', flowSet)
    return flowSetHeader

def getTemplFlowSet(flowSet):

    #  0                   1                   2                   3
    # 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
    # |       FlowSet ID = 0          |          Length              |
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
    # |      Template ID > 255        |         Field Count          |
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

    fieldCount = unpack_from('!H', flowSet, 26)
    fieldCount = fieldCount[0]

    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    # |        Field Type 1           |         Field Length 1        |
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    
    fieldFmt = '!' + 'HH' * fieldCount
    templateFlowSet = unpack_from(fieldFmt, flowSet, 28)
    return templateFlowSet

def getFlowSets(flowSet):
    #data = sock.recv(4096)
    # First unpack from bytes FlowSet header, FlowSet ID and FlowSet length.
    # Last 4 bytes added temp for testing template flowset!!!
    #
    fsHFL = unpack_from('!HHLLLLHHHHHHHHHHHHHHHHHHHHHHHHL', data)
    # `addFlow` function insert NetFlow v9 header data in Elasticsearch.
    #addFlow(index, {"version": fsHFL[0], "count": fsHFL[1], \
                        #"sysUptime": fsHFL[2], "unixSeconds": fsHFL[3], \
                            #"packageSequence": fsHFL[4], "sourceId": fsHFL[5]})
    fsd = {"version": fsHFL[0], "count": fsHFL[1], \
                        "sysUptime": fsHFL[2], "unixSeconds": fsHFL[3], \
                            "packageSequence": fsHFL[4], "sourceId": fsHFL[5]}
    # Check for FlowSet ID. Data record FlowSet ID greater than 255. 
    # Template record FlowSet ID in 0-255 range.
    if fsHFL[6] == 0:
        print(str(fsHFL))
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
            addFlow(index, fsd)

""" def startCapture(mode='unpacked'):
    # Check for capture duration.
    if clr['dur'] != 0:
        cd = time() + clr['dur']
        while time() < cd:
            getFlowSets()
    else:
        while True:
            getFlowSets() """
    
if __name__ == "__main__":
    while True:
        flowSet = sock.recv(4096)
        if getFlowSetId(flowSet) == 0:
            print(getTemplFlowSet(flowSet))