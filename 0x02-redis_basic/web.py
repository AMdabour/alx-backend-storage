#!/usr/bin/env python3
"""
web cache and tracking how many times a particular URL was accessed
"""
import redis
import requests
from functools import wraps

r = redis.Redis()


def count_url_access(method):
    """ Decorator counting how many times
    a URL is accessed """
    @wraps(method)
    def wrapper(url):
        cached_key = "cached:" + url
        cached_data = r.get(cached_key)
        if cached_data:
            return cached_data.decode("utf-8")
        count_key = "count:" + url
        r.incr(count_key)
        html = method(url)
        r.setex(cached_key, 10, html)
        return html
    return wrapper


@count_url_access
def get_page(url: str) -> str:
    """ Returns HTML content of a url """
    result = requests.get(url)
    return result.text
