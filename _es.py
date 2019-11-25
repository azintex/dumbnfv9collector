from elasticsearch import Elasticsearch
from config import es

# Elasticsearch connection object
_esco = Elasticsearch([es['connection']])

def createIndex(esObject, indexName, indexBody):
    created = False
    try:
        if not esObject.indices.exists(indexName):
            esObject.indices.create(index=indexName, ignore=400, body=indexBody)
            print('Index created')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created

def addFlow(esObject, indexName, flow):
    esObject.index(index=indexName, body=flow)

if __name__ == "__main__":
    None