from pymongo import MongoClient
from neo4j import GraphDatabase

_connection_mongo = None
_connection_neo = None

def get_mongo():
    global _connection_mongo
    if not _connection_mongo:
        _connection_mongo = MongoClient('localhost', 27017).music_explorer
    return _connection_mongo

def get_neo4j():
    global _connection_neo
    if not _connection_neo:
        _connection_neo = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "summaries+uni"))
    return _connection_neo