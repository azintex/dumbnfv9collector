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
            "ipv4SourceAddress": {
                "type": "long"
            },
            "ipv4DestinationAddress": {
                "type": "long"
            },
            "ipProtocol": {
                "type": "long"
            },
            "transportSourcePort": {
                "type": "long"
            },
            "transportDestinationPort": {
                "type": "long"
            },
            "counterBytes": {
                "type": "long"
            },
            "counterPackets": {
                "type": "long"
            },
            "timestampSysUptimeFirst": {
                "type": "long"
            },
            "timestampSysUptimeLast": {
                "type": "long"
            }
        }
    }
}

if __name__ == "__main__":
    createIndex(_es, indexName, settings)