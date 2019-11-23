from es import createIndex, _es
from datetime import date

# Default index name prefix is `netflow-v9-`
indexPrefix = 'netflow-v9-'
indexName = indexPrefix + str(date.today())

settings = {
    "settings" : {
        "number_of_shards" : 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "sysUptimeFirst": {
                "type": "text"
            },
            "sysUptimeLast": {
                "type": "text"
            },
            "counterBytes": {
                "type": "text"
            },
            "counterPackets": {
                "type": "text"
            },
            "inputInterface": {
                "type": "text"
            },
            "outputInterface": {
                "type": "text"
            },
            "ipv4SrcAddr": {
                "type": "text"
            },
            "ipv4DstAddr": {
                "type": "text"
            },
            "ipProtocol": {
                "type": "text"
            },
            "ipTos": {
                "type": "text"
            },
            "transportSrcPort": {
                "type": "text"
            },
            "transportDstPort": {
                "type": "text"
            },
            "flowSampler": {
                "type": "text"
            },
            "ipv4NextHop": {
                "type": "text"
            },
            "ipv4DstMask": {
                "type": "text"
            },
            "ipv4SrcMask": {
                "type": "text"
            },
            "tcpFlags": {
                "type": "text"
            },
            "destinationAS": {
                "type": "text"
            },
            "sourceAS": {
                "type": "text"
            }
        }
    }
}

try:
    createIndex(_es, index=indexName, body=settings)
    print('Index created')
except Exception as ex:
    print(str(ex))
finally:
    print('Index not created')