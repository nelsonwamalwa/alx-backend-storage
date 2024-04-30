#!/usr/bin/env python3
"""
changing school topic
"""
import pymongo


def update_topics(mongo_collection, name, topics):
    """
    updateing many rows
    """
    return mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )