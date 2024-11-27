from functools import lru_cache

@lru_cache
def get_config():
    return {"key": "value"}

# Clear the cache
get_config.cache_clear()
print("Cache cleared")
