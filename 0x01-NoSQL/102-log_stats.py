#!/usr/bin/env python3
"""Improve 12-log_stats.py by adding 
   the top 10 of the most present IPs 
   in the collection nginx of the database logs:"""
from pymongo import MongoClient


if __name__ == "__main__":
    '''
    providing some stats about Nginx logs
    improved by adding the top 10 of the most present IPs
    '''
    client = MongoClient('mongodb://127.0.0.1:27017')
    col = client.logs.nginx
    print("{} logs".format(col.estimated_document_count()))
    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = col.count_documents({'method': method})
        print("\tmethod {}: {}".format(method, count))
    status_get = col.count_documents({'method': 'GET', 'path': "/status"})
    print("{} status check".format(status_get))
    print("IPs:")
    topIps = col.aggregate([
        {"$group":
            {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "ip": "$_id",
            "count": 1
        }}
    ])
    for ip in topIps:
        print("\t{}: {}".format(ip.get('ip'), ip.get('count')))