# Overview
Rough couple of scripts to handle moving / renaming TV episodes downloaded from usenet. I'll clean these up eventually, but they work pretty well at the moment. Of course they crash spectacularly if any number of assumptions don't hold, but whatever.

# tvfilterone.py
Pulls all of the actual episodes from a single directory, renames, and moves to a given path.

`python tvfilterone.py <directory to search> <threshold size in bytes> <path prefix to move to>`

# tvfiltermulti.py
Searches the given directory for basically single episodes contained in directories.

`python tvfiltermulti.py <directory to search> <path prefix to move to>`

# scraper.py
Right now, just scrapes a wikipedia list-of-episodes document for episode names. Returns a map, like:
`metadata[<season number>][<episode number>]`

# renamer.py
renamer.py renames files in the given directory (filenames are assumed to be in the format created by the tvfilter*.py) using the metadata provided.

metadata is scraped using scraper.py.


`renamer.renameAll(<path of the episode files>, <metadata stream>)`

