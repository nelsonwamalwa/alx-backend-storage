#!/usr/bin/env python3
"""
This cntains the class definition for redis cache
"""
import redis
import uuid
from functools import wraps
from typing import Union, Callable, Optional


def count_calls(method: Callable) -> Callable:
    """
    This counts the number of times a function is called
    Args:
        method:Function to be decorated
    Returns:
        Decorated function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        A wrapper function for the decorated function
        Args:
            self: Object instance
            *args: Arguments passed to the function
            **kwargs: Keyword arguments passed to the function
        Returns:
            Return value of the decorated function
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Counting the number of times a function is called
    Args:
        method: Function to be decorated
    Returns:
        Our decorated function
    """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        A wrapper function for the decorated function
        Args:
            self: Object instance
            *args: Arguments passed to the function
            **kwargs: Keyword arguments passed to the function
        Returns:
            Returning value of the decorated function
        """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data

    return wrapper


def replay(method: Callable) -> None:
    """
    Replaying the history of a function
    Args:
        method: Function to be decorated
    Returns:
        None
    """
    name = method.__qualname__
    cache = redis.Redis()
    calls = cache.get(name).decode("utf-8")
    print("{} was called {} times:".format(name, calls))
    inputs = cache.lrange(name + ":inputs", 0, -1)
    outputs = cache.lrange(name + ":outputs", 0, -1)
    for i, o in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(name, i.decode('utf-8'),
                                     o.decode('utf-8')))


class Cache:
    """
    Defining methods to handle redis cache operations
    """
    def __init__(self) -> None:
        """
        Initializing redis client
        Attributes:
            self._redis (redis.Redis): redis client
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores data in redis cache
        Args:
            data (dict): The data to store
        Returns:
            str: key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None)\
            -> Union[str, bytes, int, float, None]:
        """
        Getting data from redis cache
        """
        data = self._redis.get(key)
        if data is not None and fn is not None and callable(fn):
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Getting data as string from redis cache
        Args:
            key (str): key
        Returns:
            str: data
        """
        data = self.get(key, lambda x: x.decode('utf-8'))
        return data

    def get_int(self, key: str) -> int:
        """
        Getting data as integer from redis cache
        Args:
            key (str): key
        Returns:
            int: data
        """
        data = self