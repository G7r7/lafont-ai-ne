from gutenbergpy.gutenbergcache import GutenbergCache
from gutenbergpy.gutenbergcache import GutenbergCacheSettings
import requests

GutenbergCacheSettings.set( CacheFilename="gutenbergindex.db")

GutenbergCache.create()

cache  = GutenbergCache.get_cache()

links = list(cache.native_query('select downloadlinks.name, books.gutenbergbookid \
  from books\
  left join bookshelves on bookshelves.id = books.bookshelveid\
  left join downloadlinks on books.id = downloadlinks.bookid\
  left join downloadlinkstype on downloadlinks.downloadtypeid = downloadlinkstype.id\
  WHERE\
  bookshelves.name like "FR Po%sie" AND\
  downloadlinkstype.name = "text/plain; charset=utf-8" AND\
  downloadlinks.name like "%.txt"'))

for link in links:
  file = requests.get(link[0])
  print(link[1])
  open('texts/'+str(link[1])+'.txt','wb').write(file.content)

