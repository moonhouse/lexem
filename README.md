# Lexem
Create a Bloom filter with lexemes from a Wikidata data dump 
(latest-lexemes.json.gz) and then use that to check if a dataset from the 
Swedish parliament contains words not already included.

## Steps for getting started
### Download lexemes dump 
As of July 2023 this file is around 400 MiB large.
````bash
curl -O https://dumps.wikimedia.org/wikidatawiki/entities/latest-lexemes.json.gz
````
### Install dependencies
````bash
pipenv install 
````
### Populate Bloom filter
````bash
pipenv run python create_bloom.py
````
### Download parliament transcripts
````bash
curl -O https://data.riksdagen.se/dataset/dokument/mot-2018-2021.json.zip
````

