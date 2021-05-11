config = {
    'general': {
        'http': {
            'timeout': 120
        },
        'dbpedia': {
            'endpoint': 'http://dbpedia.org/sparql',
            # 'endpoint': 'https://query.wikidata.org/',  # wikidata
            # 'endpoint': 'http://sam01dbpedia:sam@192.168.0.10/sparql',  # localhost or doker
            'one_hop_bloom_file': './data/blooms/spo1.bloom',
            'two_hop_bloom_file': './data/blooms/spo2.bloom'
        }
    }
}
