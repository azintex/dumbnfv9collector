from elasticsearch import Elasticsearch
from config import es

# Elasticsearch connection object
_esco = Elasticsearch([es['connection']])

def createIndex(indexName, indexBody):
    created = False
    try:
        if not _esco.indices.exists(indexName):
            _esco.indices.create(index=indexName, ignore=400, body=indexBody)
            print('Index created')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created

def addFlow(indexName, flow):
    _esco.index(index=indexName, body=flow)

if __name__ == "__main__":
    None