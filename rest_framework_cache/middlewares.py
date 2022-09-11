"""
middlewares for caching.
"""

from django.core.cache import cache

CACHE_KEY_ATTRIBUTE = "_cache_key"


class RestFrameworkCacheMiddleware:
    """
    middleware to cache successful responses based on the key provided by the
    decorators.
    """

    def __caching(self, response):
        if hasattr(response, CACHE_KEY_ATTRIBUTE) and response.status_code == 200:
            key = getattr(response, CACHE_KEY_ATTRIBUTE)

            delattr(response, CACHE_KEY_ATTRIBUTE)
            cache.set(key, response)

        return response

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.__caching(self.get_response(request))
