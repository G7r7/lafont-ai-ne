from gutenbergpy.gutenbergcache import GutenbergCache
#for sqlite
GutenbergCache.create(refresh=True, download=True, unpack=True, parse=True, cache=True, deleteTemp=True)

cache  = GutenbergCache.get_cache()

print(cache.native_query("SELECT Distinct * FROM languages"))

print(cache.native_query("SELECT Distinct * FROM types"))