#!/usr/bin/env python3
'''Implementing an expiring web cache and tracker
'''
import redis
import requests
from datetime import timedelta


def get_page(url: str) -> str:
    '''This returns the content of a URL after caching the request's response,
    and tracking the request.
    '''
    if url is None or len(url.strip()) == 0:
        return ''
    redis_store = redis.Redis()
    res_key = 'result:{}'.format(url)
    req_key = 'count:{}'.format(url)
    result = redis_store.get(res_key)
    if result is not None:
        redis_store.incr(req_key)
        return result.decode('utf-8')  # Decode the result if it's retrieved from Redis
    result = requests.get(url).content.decode('utf-8')
    redis_store.setex(res_key, timedelta(seconds=10), result)
    return result
