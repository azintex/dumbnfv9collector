from datetime import date

# Collector config options :
    # mode = @str 
    # `raw` get all FlowSets and store in binary file which then may be parsed.
    # `unpacked` get only data record FlowSets and write to Elasticsearch.
    # Default mode `unpacked`

    # ip_address = @str 
    # Define listen IPv4 address.

    # port = @int
    # Define listen port.

    # ts = @int
    # Data record FlowSet template size in bytes.
    # Information about data record FlowSet template may be obtained from exporter device. 
    # e.g. on Cisco ASR 1002-X : router#show flow monitor {MONITOR_NAME} templates details

    # dur = @int
    # Capture duration time in seconds.  
clr = {
    'mode': 'unpacked',
    'ip_address': '172.16.93.5',
    'port': 2055,
    'ts': 29,
    'dur': 120
}


# Elasticsearch config options :
    # host = @str

    # port = @int

    # index :
    # prefix = @str
    # name = @str
es = {
    'connection': {
        'host' : 'localhost',
        'port': 9200
    },
    'index': {
        'prefix': 'test-',
        'name': str(date.today())
    }
}