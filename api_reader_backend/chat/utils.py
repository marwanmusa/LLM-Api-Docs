from django.core.cache import cache
from django.conf import settings
import json
import hashlib

def get_cache_key(prefix, *args, **kwargs):
    """Generate a unique cache key based on arguments."""
    # Convert args and kwargs to a string representation
    key_parts = [str(arg) for arg in args]
    key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
    key_string = ":".join(key_parts)
    
    # Create a hash of the key string
    key_hash = hashlib.md5(key_string.encode()).hexdigest()
    return f"{prefix}:{key_hash}"

def cache_api_response(prefix, ttl=None):
    """Decorator to cache API responses."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            cache_key = get_cache_key(prefix, *args, **kwargs)
            cached_response = cache.get(cache_key)
            
            if cached_response is not None:
                return cached_response
            
            response = func(*args, **kwargs)
            cache.set(cache_key, response, timeout=ttl or settings.CACHE_TTL)
            return response
        return wrapper
    return decorator

def cache_vector_data(api_doc_id, content, vector_data):
    """Cache vector data for API documentation."""
    cache_key = f"vector:{api_doc_id}:{hashlib.md5(content.encode()).hexdigest()}"
    cache.set(cache_key, vector_data, timeout=settings.VECTOR_CACHE_TTL)
    return cache_key

def get_cached_vector(api_doc_id, content):
    """Retrieve cached vector data."""
    cache_key = f"vector:{api_doc_id}:{hashlib.md5(content.encode()).hexdigest()}"
    return cache.get(cache_key)

def invalidate_api_cache(prefix):
    """Invalidate all cache entries with a specific prefix."""
    pattern = f"{prefix}:*"
    keys = cache.keys(pattern)
    if keys:
        cache.delete_many(keys)

def cache_conversation_history(conversation_id, messages, ttl=None):
    """Cache conversation history."""
    cache_key = f"conversation:{conversation_id}"
    cache.set(cache_key, messages, timeout=ttl or settings.CACHE_TTL)

def get_cached_conversation(conversation_id):
    """Retrieve cached conversation history."""
    cache_key = f"conversation:{conversation_id}"
    return cache.get(cache_key)

def clear_conversation_cache(conversation_id):
    """Clear cached conversation history."""
    cache_key = f"conversation:{conversation_id}"
    cache.delete(cache_key) 