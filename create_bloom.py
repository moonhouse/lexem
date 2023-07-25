import gzip
import json
from distutils.log import error

from bloom_filter2 import BloomFilter

values = 0
bloom = BloomFilter(max_elements=227830, error_rate=0.1, filename="svenska.bf")

with gzip.open("latest-lexemes.json.gz", 'rt') as lexemes:
    for line in lexemes:
        if '"language":"sv"' in line:
            line = line.rstrip(",\n")
            data = json.loads(line)
            if 'sv' in data['lemmas']:
                forms = [x['representations']['sv']['value']
                         for x in data['forms']]
                forms.append(data['lemmas']['sv']['value'])
                unique = list(set(forms))
                for word in unique:
                    bloom.add(word)
                values += len(unique)
                # print(list(set(forms)))
    print(values)
