#!/usr/bin/env python3
"""
find school by topic
"""
import pymongo


def schools_by_topic(mongo_collection, topic):
    """
    Finding by topic
    """
    return mongo_collection.find({"topics": topic})