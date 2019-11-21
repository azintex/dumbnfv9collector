from elasticsearch import Elasticsearch

_es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def connectElasticSearch(host=str, port=int):
    __es = None
    __es = Elasticsearch([{"host": host, "port": port}])
    if _es.ping():
        print('Pinged')
    else:
        print('No ping')
    return __es

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