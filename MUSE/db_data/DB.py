from neo4j import GraphDatabase

_connection_mongo = None
_connection_neo = None

def get_neo4j():
    global _connection_neo
    if not _connection_neo:
        _connection_neo = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "summaries+uni"))
    return _connection_neo