from datetime import date
from struct import unpack, unpack_from, iter_unpack
from socket import socket, AF_INET, SOCK_DGRAM
from es import addFlow, _es
import json

indexPrefix = 'netflow-v9-'
indexName = indexPrefix + str(date.today())

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(('172.16.93.5', 2055))

if __name__ == "__main__":
    while True:
        data = sock.recv(4096)
        fsHeader = unpack('!HHLLLL', data[:20])
        #addFlow(_es, indexName, json.dumps(fsHeader))
        fsId = unpack('!H', data[20:22])
        if fsId[0] == 0:
            fsTemplate = unpack_from('!H*22', data, 22)
            print(type(fsTemplate[0]))
            #addFlow(_es, indexName, json.dumps(fsTemplate))
        else:        
            fs = unpack_from('!LLBHHLLLL', data, 24)
            print(type(fs[0]))
            #addFlow(_es, indexName, json.dumps(fsHeader))