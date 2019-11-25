from elasticsearch import Elasticsearch
from config import es

# Elasticsearch connection object
_esco = Elasticsearch([es['connection']])
# Elasticsearch index settings
_settings = {
    "settings": {
        "index": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }
    }
}

def createIndex(_index, _body):
    created = False
    try:
        if not _esco.indices.exists(_index):
            _esco.indices.create(index=_index, ignore=400, body=_body)        
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created

def addFlow(_index, _body):
    if createIndex(_index, _settings) != False:
        _esco.index(index=_index, body=_body)

if __name__ == "__main__":
    None