#!/usr/bin/env python3
"""
creating a cache class and storing
an instance of Redis client in it
"""
import redis
from typing import Union
from uuid import uuid4


class Cache():
    """Cache class"""
    def __init__(self) -> None:
        """initializing the any instance of the class with
        redis client object"""
        self._redis: object = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """store method"""
        key = str(uuid4())
        self._redis.set(key, data)
        return key
