from struct import unpack, unpack_from, iter_unpack
from socket import socket, AF_INET, SOCK_DGRAM

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(('172.16.93.5', 2055))

if __name__ == "__main__":
    while True:
        data = sock.recv(1522)
        # Flow header
        fh = unpack('!HHLLLL', data[0:20])
        # FlowSet
        fs = unpack('!HHHH', data[20:28])
        print(str(fh + '|' + fs))