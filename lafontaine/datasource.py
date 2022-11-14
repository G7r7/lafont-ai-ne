#!/usr/bin/env python3

from gutenbergpy.gutenbergcache import GutenbergCache
from gutenbergpy.gutenbergcache import GutenbergCacheSettings
import requests
from cleaning import strip_headers
import re

from pathlib import Path

def download_dataset():
    APP_DIR = Path.home() / ".lafontaine"
    CACHE_DIR = APP_DIR / "cache"
    TEXT_DIR = CACHE_DIR / "text"
    DATASET = APP_DIR / "dataset.txt"

    APP_DIR.mkdir(exist_ok=True, parents=True)
    CACHE_DIR.mkdir(exist_ok=True)
    TEXT_DIR.mkdir(exist_ok=True)
    CACHE_FILE = CACHE_DIR / "gutenbergindex.db"
    DATASET.touch(exist_ok=True)

    GutenbergCacheSettings.set(CacheFilename=CACHE_FILE)
    GutenbergCache.create()

    cache  = GutenbergCache.get_cache()

    links = list(cache.native_query('select downloadlinks.name, books.gutenbergbookid\
    from books\
    left join bookshelves on bookshelves.id = books.bookshelveid\
    left join downloadlinks on books.id = downloadlinks.bookid\
    left join downloadlinkstype on downloadlinks.downloadtypeid = downloadlinkstype.id\
    WHERE\
    bookshelves.name like "FR Po%sie" AND\
    downloadlinkstype.name = "text/plain; charset=utf-8" AND\
    downloadlinks.name like "%.txt" AND\
    books.gutenbergbookid not in (17590, 62922,62508,60738,60417,58317,56708,54419,53761,52629,52065,51120,46991,46687,45312,33595,20640,20479)'))

    nb_links = len(links)
    for i, link in enumerate(links):
        print(f"{i} / {nb_links}")
        pg_number = link[1]

        file = TEXT_DIR / f"PG{pg_number}.txt"
        if file.exists():
            continue
        
        r = requests.get(link[0])
        content = r.content.decode("utf-8")
        cleaned = strip_headers(content)

        with file.open("w") as stream:
            stream.write(cleaned)

    verses = []

    for file in TEXT_DIR.glob("*.txt"):
        with file.open("r") as stream:
            text = stream.read()
            paragraphes = re.split(r"\n{2,}", text)
            
            for paragraphe in paragraphes:
                if paragraphe.count('\n') > 1:
                    for line in paragraphe.splitlines():
                        stripped = line.strip() # remove leading and trailing whitespaces
                        if stripped.split(' ')[0].isupper():
                            continue # ignore if first word is all uppercase
                        verses.append(f"{stripped}\n")

    with DATASET.open("a") as output:
        output.writelines(verses)
