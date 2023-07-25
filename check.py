from distutils.log import error

from bloom_filter2 import BloomFilter

bloom = BloomFilter(max_elements=227830, error_rate=0.1, filename="svenska.bf")

for word in ['Sverige', 'nuläget', 'jag']:
    print(word in bloom)
