from zipfile import ZipFile
import json
import lxml.html
from itertools import chain
from bloom_filter2 import BloomFilter
import string
import re
from collections import Counter


my_punctuation = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~\u00ad”'
bloom = BloomFilter(max_elements=227830, error_rate=0.1, filename="svenska.bf")
wc = Counter()

with ZipFile('mot-2018-2021.json.zip') as myzip:
    motioner = myzip.namelist()
    for motion_filename in motioner:
        with myzip.open(motion_filename, mode='r') as motion_file:
            motion = json.loads(motion_file.read().decode('utf-8'))
            html = lxml.html.fromstring(motion['dokumentstatus']['dokument']['html'])
            if 'Motionen utgår.' in html.text_content():
                continue
            for bad in html.xpath("//style"):
                bad.getparent().remove(bad)

            try:

                preceding_one = html.xpath("//*[@class='Section1']")[0].itersiblings(preceding=True)
                
                if len(html.xpath("//*[@style='-aw-sdt-tag:CC_Underskrifter; -aw-sdt-title:CC_Underskrifter']")) > 0:            
                    following = html.xpath("//*[@style='-aw-sdt-tag:CC_Underskrifter; -aw-sdt-title:CC_Underskrifter']")[0].itersiblings()
                else:
                    following = html.xpath("//*[@class='Underskrifter']")[0].itersiblings()


                if len(html.xpath("//*[@class='Frslagstext']")) > 0:
                    preceding_two = html.xpath("//*[@class='Frslagstext']")[0].itersiblings(preceding=True)
                else:
                    preceding_two = iter([])

                motivering = html.xpath("//a[@name='MotionsStart']")[0].itersiblings()

                generator = chain(preceding_one, preceding_two, following, motivering)

                for tag in generator:
                    tag.getparent().remove(tag)

                plaintext = html.text_content().strip()

                words = list(set(plaintext.translate(str.maketrans('', '', my_punctuation)).split()))
                words = filter(lambda word: not bool(re.search(r'\d', word)), words)
                missing_words = []
                for word in words:
                    if not word.lower() in bloom and not word in bloom:
                        missing_words.append(word)
                wc.update(missing_words)

            except IndexError as err:
                print(f"Unexpected {err=}, {type(err)=}")
                print(f"{motion_filename}")
print(wc.most_common(250))
