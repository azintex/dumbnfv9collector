from struct import unpack, unpack_from, iter_unpack
from socket import socket, AF_INET, SOCK_DGRAM

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(('172.16.93.5', 2055))

if __name__ == "__main__":
    while True:
        data = sock.recv(4096)
        # Flow header
        #fh = unpack('!HHLLLL', data[0:20])
        # FlowSet ID
        fsId = unpack('!H', data[20:22])
        print(str(fsId))
        # Template FlowSet
        #tfs = unpack('!HH', data[20:24])
        # FlowSet
        #fs = unpack('!HHHH', data[20:28])
        #print(str(fs))