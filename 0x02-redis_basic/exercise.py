#!/usr/bin/env python3
"""
creating a cache class and storing
an instance of Redis client in it
"""
from redis import Redis
from typing import Union, Optional, Callable
from uuid import uuid4
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """count the num of calls of a class method"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper function"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache():
    """Cache class"""
    def __init__(self):
        """initializing the any instance of the class with
        redis client object"""
        self._redis = Redis(host="localhost", port="6379", db=0)
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """store method"""
        key: str = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """convert the data back to the desired format"""
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """convert data to string format"""
        value = self._redis.get(key).decode("utf-8")
        return value

    def get_int(self, key: str) -> int:
        """convert data to integer format"""
        value = int(self._redis.get(key).decode("utf-8"))
        return value
