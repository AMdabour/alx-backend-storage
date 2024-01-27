#!/usr/bin/env python3
"""
creating a cache class and storing
an instance of Redis client in it
"""
from redis import Redis
from typing import Union, Optional, Callable
from uuid import uuid4


class Cache():
    """Cache class"""
    def __init__(self):
        """initializing the any instance of the class with
        redis client object"""
        self._redis = Redis(host="localhost", port="6379", db=0)
        self._redis.flushdb()

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
