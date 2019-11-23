import os, socket, sys
from struct import unpack, unpack_from
from datetime import date
from time import time
import config as cfg
from es import createIndex, addFlow, _es

templSize = cfg.template_size_in_bytes

if cfg.capture_duration != 0:
    captDur = time() + cfg.caption_duration

# Socket initialization
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Socket binding
sock.bind((cfg.ip_address, cfg.port))

# Date stamps
td = str(date.today())

def startCapture(mode):
    if not os.path.exists('dumps') and mode == 'raw':
        os.mkdir('dumps')

    if not os.path.exists('flows') and mode == 'unpack':
        os.mkdir('flows')

    if os.path.exists('dumps') and mode == 'raw':
        os.chdir('dumps')
        #dump = open(td + '.dump', 'wb')
    elif os.path.exists('flows') and mode == 'unpack':
        os.chdir('flows')
        #ff = open(td + '-flows.txt', 'w')

    while mode == 'raw' and time() < captDur:
        data = sock.recv(1518)
        print(data)
    
    # captDur set capture duration in seconds, in case is not exist capture will be infinity

    try:
        if not captDur:
            while True:
                data = sock.recv(1522)
                flowHeader = struct.unpack('!HHLLLL', data[0:20])

                for flow in range(0, flowHeader[1]):
                    if flow == 0:
                        firstFlow = struct.unpack('!IIIIIIIIBBHHBIBBBHH', data[24:74])
                        addFlow(_es, 'netflow-v9', {"sysUptimeFirst": firstFlow[0], "sysUptimeLast": firstFlow[1], "counterBytes": firstFlow[2], \
                            "counterPackets": firstFlow[3], "inputInterface": firstFlow[4], "outputInterface": firstFlow[5], "ipv4SrcAddr": firstFlow[6], \
                                "ipv4DstAddr": firstFlow[7], "ipProtocol": firstFlow[8], "ipTos": firstFlow[9], "transportSrcPort": firstFlow[10], \
                                    "transportDstPort": firstFlow[11], "flowSampler": firstFlow[12], "ipv4NextHop": firstFlow[13], "ipv4DstMask": firstFlow[14], \
                                        "ipv4SrcMask": firstFlow[15], "tcpFlags": firstFlow[16], "destinationAS": firstFlow[17], "sourceAS": firstFlow[18]})
                    else:
                        offset = flow * templSize
                        subseqFlow = struct.unpack('!IIIIIIIIBBHHBIBBBHH', data[24 + offset:74 + offset])
                        addFlow(_es, 'netflow-v9', {"sysUptimeFirst": subseqFlow[0], "sysUptimeLast": subseqFlow[1], "counterBytes": subseqFlow[2], \
                            "counterPackets": subseqFlow[3], "inputInterface": subseqFlow[4], "outputInterface": subseqFlow[5], "ipv4SrcAddr": subseqFlow[6], \
                                "ipv4DstAddr": subseqFlow[7], "ipProtocol": subseqFlow[8], "ipTos": subseqFlow[9], "transportSrcPort": subseqFlow[10], \
                                    "transportDstPort": subseqFlow[11], "flowSampler": subseqFlow[12], "ipv4NextHop": subseqFlow[13], "ipv4DstMask": subseqFlow[14], \
                                        "ipv4SrcMask": subseqFlow[15], "tcpFlags": subseqFlow[16], "destinationAS": subseqFlow[17], "sourceAS": subseqFlow[18]})
    finally:
        while time() < cfg.capture_duration:
            data = sock.recv(1522)
            flowHeader = struct.unpack('!HHLLLL', data[0:20])

            for flow in range(0, flowHeader[1]):
                if flow == 0:
                    firstFlow = struct.unpack('!IIIIIIIIBBHHBIBBBHH', data[24:74])
                    addFlow(_es, 'netflow-v9', {"sysUptimeFirst": firstFlow[0], "sysUptimeLast": firstFlow[1], "counterBytes": firstFlow[2], \
                        "counterPackets": firstFlow[3], "inputInterface": firstFlow[4], "outputInterface": firstFlow[5], "ipv4SrcAddr": firstFlow[6], \
                            "ipv4DstAddr": firstFlow[7], "ipProtocol": firstFlow[8], "ipTos": firstFlow[9], "transportSrcPort": firstFlow[10], \
                                "transportDstPort": firstFlow[11], "flowSampler": firstFlow[12], "ipv4NextHop": firstFlow[13], "ipv4DstMask": firstFlow[14], \
                                    "ipv4SrcMask": firstFlow[15], "tcpFlags": firstFlow[16], "destinationAS": firstFlow[17], "sourceAS": firstFlow[18]})
                else:
                    offset = flow * templSize
                    subseqFlow = struct.unpack('!IIIIIIIIBBHHBIBBBHH', data[24 + offset:74 + offset])
                    addFlow(_es, 'netflow-v9', {"sysUptimeFirst": subseqFlow[0], "sysUptimeLast": subseqFlow[1], "counterBytes": subseqFlow[2], \
                        "counterPackets": subseqFlow[3], "inputInterface": subseqFlow[4], "outputInterface": subseqFlow[5], "ipv4SrcAddr": subseqFlow[6], \
                            "ipv4DstAddr": subseqFlow[7], "ipProtocol": subseqFlow[8], "ipTos": subseqFlow[9], "transportSrcPort": subseqFlow[10], \
                                "transportDstPort": subseqFlow[11], "flowSampler": subseqFlow[12], "ipv4NextHop": subseqFlow[13], "ipv4DstMask": subseqFlow[14], \
                                    "ipv4SrcMask": subseqFlow[15], "tcpFlags": subseqFlow[16], "destinationAS": subseqFlow[17], "sourceAS": subseqFlow[18]})

if __name__ == '__main__':
    startCapture(cfg.mode)