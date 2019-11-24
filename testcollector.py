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
        fsHeader = unpack_from('!HHLLLLHH', data)
        """ addFlow(_es, indexName, {"version": fsHeader[0], "count": fsHeader[1], \
                                    "sysUptime": fsHeader[2], "unixSeconds": fsHeader[3], \
                                        "packageSequence": fsHeader[4], "sourceId": fsHeader[5]}) """
        #fsId = unpack('!H', data[20:22])
        if fsHeader[6] != 0:
            #fs = iter_unpack('!LLBHHLLLL', data[24:fsHeader[7] - 5])    
            print(str(fsHeader[7]))
        """ if fsId[0] == 0:
            fsTemplate = unpack_from('!HHHHHHHHHHHHHHHHHHHHHH', data, 22)            
            #addFlow(_es, indexName, )
            print(str(fsTemplate))
        else:
            # Resolve this error : elasticsearch.exceptions.RequestError: RequestError(400, 'mapper_parsing_exception', "failed to parse field [timestampSysUptimeLast] of type [integer] in document with id 'GNLUmm4BFQEDuzdY5Eis'. Preview of field's value: '3286266866'")
            fs = unpack_from('!LLBHHLLLL', data, 24)
            addFlow(_es, indexName, {"ipv4SourceAddress": fs[0], \
                                        "ipv4DestinationAddress": fs[1], \
                                            "ipProtocol": fs[2], \
                                                "transportSourcePort": fs[3], \
                                                    "transportDestinationPort": fs[4], \
                                                        "counterBytes": fs[5], \
                                                            "counterPackets": fs[6], \
                                                                "timestampSysUptimeFirst": fs[7], \
                                                                    "timestampSysUptimeLast": fs[8]}) """