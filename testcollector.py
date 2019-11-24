from datetime import date
from struct import unpack, unpack_from, iter_unpack
from socket import socket, AF_INET, SOCK_DGRAM
from es import addFlow, _es
from create_es_index import settings
import json

indexPrefix = 'netflow-v9-'
indexName = indexPrefix + str(date.today())

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(('172.16.93.5', 2055))

if __name__ == "__main__":
    while True:
        data = sock.recv(4096)
        # First unpack from bytes FlowSet header, FlowSet ID and FlowSet length.
        fsHFL = unpack_from('!HHLLLLHH', data)
        # Insert data in Elasticsearch.
        addFlow(_es, indexName, {"version": fsHFL[0], "count": fsHFL[1], \
                                    "sysUptime": fsHFL[2], "unixSeconds": fsHFL[3], \
                                        "packageSequence": fsHFL[4], "sourceId": fsHFL[5]})
        # Check for FlowSet ID. Data record FlowSet ID greater than 255. 
        # Template record FlowSet ID in 0-255 range.
        if fsHFL[6] != 0:
            # First get unpacked iterable. 
            # The buffer’s size in bytes must be a multiple of the size required by the format (c)
            fs = iter_unpack('!LLBHHLLLL', data[24:fsHFL[1] * 29 + 24])
            for flow in fs:
                addFlow(_es, indexName, {"ipv4SourceAddress": flow[0], \
                                            "ipv4DestinationAddress": flow[1], \
                                                "ipProtocol": flow[2], \
                                                    "transportSourcePort": flow[3], \
                                                        "transportDestinationPort": flow[4], \
                                                            "counterBytes": flow[5], \
                                                                "counterPackets": flow[6], \
                                                                    "timestampSysUptimeFirst": flow[7], \
                                                                        "timestampSysUptimeLast": flow[8]})