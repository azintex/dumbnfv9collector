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
                "type": "integer"
            },
            "ipv4DestinationAddress": {
                "type": "integer"
            },
            "ipProtocol": {
                "type": "integer"
            },
            "transportSourcePort": {
                "type": "integer"
            },
            "transportDestinationPort": {
                "type": "integer"
            },
            "counterBytes": {
                "type": "integer"
            },
            "counterPackets": {
                "type": "integer"
            },
            "timestampSysUptimeFirst": {
                "type": "integer"
            },
            "timestampSysUptimeLast": {
                "type": "integer"
            }
        }
    }
}

if __name__ == "__main__":
    createIndex(_es, indexName, settings)