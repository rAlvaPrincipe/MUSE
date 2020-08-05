from db_data import DB as db
driver = db.get_neo4j()


def insert_node(list_related_to):
    with driver.session() as session:
        tx = session.begin_transaction()
        for couple in  list_related_to:
            if couple[1] is None:
                tx.run("MERGE (a:Person {name: $name}) ",
                       name=couple[0])
            else:
                tx.run("MERGE (a:Person {name: $name}) "
                       "MERGE (b:Person {name: $friend_name}) "
                       "MERGE (a)-[:KNOWS]->(b)",
                       name=couple[0], friend_name=couple[1])
        tx.commit()


def insert_node2(list_related_to):
    with driver.session() as session:
        tx = session.begin_transaction()
        for couple in  list_related_to:
            if couple[1] is None:
                tx.run("MERGE (a:Person {URL: $URL, label: $label, label_ext: $label_ext}) ",
                       URL=couple[0]["_id"], label=couple[0]["label"], label_ext=couple[0]["label_ext"])
            else:
                tx.run("MERGE (a:Person {URL: $URL_a, label: $label_a, label_ext: $label_ext_a}) "
                       "MERGE (b:Person {URL: $URL_b, label: $label_b, label_ext: $label_ext_b}) "
                       "MERGE (a)-[:KNOWS]->(b)",
                       URL_a=couple[0]["_id"], label_a=couple[0]["label"], label_ext_a=couple[0]["label_ext"],
                       URL_b=couple[1]["_id"], label_b=couple[1]["label"], label_ext_b=couple[1]["label_ext"])
        tx.commit()



# takes a list of couples of strings (artist ids)
def influenced_by(list_influenced_by, relation):
    with driver.session() as session:
        tx = session.begin_transaction()
        for couple in  list_influenced_by:
            tx.run("MATCH (a:Person), (b:Person) "
                   "WHERE a.URL = $URL_a AND b.URL = $URL_b "
                   "MERGE (a)-[:" + relation + "]->(b)",
                   URL_a=couple[0], URL_b=couple[1])
        tx.commit()


def connections_from(id, relation):
    with driver.session() as session:
        tx = session.begin_transaction()
        res = tx.run("MATCH (a {URL:$id})-[:"+ relation + "]->(b)"
                     "RETURN b",
                     id=id)
        tx.commit()
    return res


def connections_to(id, relation):
    with driver.session() as session:
        tx = session.begin_transaction()
        res = tx.run("MATCH (b)-[:" + relation + "]->(a {URL:$id})"
                     "RETURN b",
                     id=id)
        tx.commit()
    return res

def related_to(artist_id, bidirectional):
    res = connections_from(artist_id, "KNOWS")
    connections = list()
    for record in res:
        connections.append((record["b"]["URL"], record["b"]["label"]))
    if bidirectional:
        res = connections_to(artist_id, "KNOWS")
        for record in res:
            connections.append((record["b"]["URL"], record["b"]["label"]))
    return connections


def linked_to(artist_id, relation, bidirectional):
    res = connections_from(artist_id, relation)
    connections = list()
    for record in res:
        connections.append((record["b"]["URL"], record["b"]["label"]))
    if bidirectional:
        res = connections_to(artist_id, relation)
        for record in res:
            connections.append((record["b"]["URL"], record["b"]["label"]))
    return connections


#----------------------------------

def hold(relation, source, target):
    #print(source + "  " + target)
    with driver.session() as session:
        tx = session.begin_transaction()
        res = tx.run("MATCH (a {URL:\"" + source +"\" })-[r :"+ relation + "]->(b {URL:\"" + target + "\"}) "
                     "RETURN a",
        )
        tx.commit()
    return res

def get_nodes():
    with driver.session() as session:
        tx = session.begin_transaction()
        res = tx.run("MATCH (b:Person) "
                     "RETURN b ",
        )
        tx.commit()
    return res




#'''
res = get_nodes()
nodes = list()
for record in res:
    nodes.append((record["b"]["URL"]))

print(len(nodes))

contributions_n = 0
for node in nodes:
    print(contributions_n, " " + node )
    connections = linked_to(node, "inf_ML_by", False)
    for connection in connections:
        res2 = hold("inflooenz_by", node, connection[0])
        if len(list(res2)) == 0:
            contributions_n += 1
print("total contributions:")
print(contributions_n)
#'''

