from gutenbergpy.gutenbergcache import GutenbergCache
from gutenbergpy.gutenbergcache import GutenbergCacheSettings
import requests
from cleaning import cleanup
from selection import poem_selection
import os

GutenbergCacheSettings.set( CacheFilename="gutenbergindex.db")

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
  books.gutenbergbookid not in (62922,62508,60738,60417,58317,56708,54419,53761,52629,52065,51120,46991,46687,45312,33595,20640,20479) '))

for link in links:
  file = requests.get(link[0])
  print(link[1])
  with open('texts/PG'+str(link[1])+'_raw.txt','wb') as file_stream:
    file_stream.write(file.content)


for(dirpath, dirnames, filenames) in os.walk("texts/"):
  for filename in filenames:
    path = os.path.join(dirpath, filename)
    if filename.endswith('.txt'):
      cleanup(path,"clean_texts/")


for(dirpath, dirnames, filenames) in os.walk("clean_texts/"):
  for filename in filenames:
    print(filename)
    path = os.path.join(dirpath, filename)
    poem_selection(path, filename)
    
  
