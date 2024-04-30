#!/usr/bin/env python3
"""
This module has a utility function that lists all documents
"""
import pymongo


def list_all(mongo_collection):
    """
    List all documents in a collection
    """
    if mongo_collection is None:
        return []

    return list(mongo_collection.find())
