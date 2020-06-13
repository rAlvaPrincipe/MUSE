import DB as db

artists = db.get_mongo().all_artists
driver = db.get_neo4j()

def find_all(linked):
    if linked:
        return artists.find({"linked":True})
    elif linked is False:
        return artists.find({"linked": False})
    elif linked is None:
        return artists.find({})

# returns a dict
def find_by_id(id):
    return artists.find_one({'_id': id})

def find_by_label_ext(label_ext):
    return artists.find_one({'label_ext': label_ext})

def exists(id):
    return not (artists.find({'_id': id}).count() == 0)

def insert(artist):
   if not  exists(artist._id):
       artists.insert_one(artist.__dict__)

def replace(artist):
    if type(artist) is dict:
        artists.replace_one({'_id': artist["_id"]}, artist, upsert=True)
    else:
        artists.replace_one({'_id': artist._id}, artist.__dict__, upsert=True)


def find_too_similars():
    print("dentro")
    labels = set()
    for el in find_all():
        if labels.__contains__(el["label"]):
            print(el['_id'] + " " +el['label'])
        else:
            labels.add(el["label"])

    return labels.__len__()



#def bulk_load(artists):
#    artist.insert_many([ob.__dict__ for ob in artists])

#------------------------------------------------------------------------- Neo 4j

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


def connections_from(id):
    with driver.session() as session:
        tx = session.begin_transaction()
        res = tx.run("MATCH (a {URL:$id})-[:KNOWS]->(b)"
                     "RETURN b",
                     id=id)
        tx.commit()
    return res

def connections_to(id):
    with driver.session() as session:
        tx = session.begin_transaction()
        res = tx.run("MATCH (a)-[:KNOWS]->(b {URL:$id})"
                     "RETURN a",
                     id=id)
        tx.commit()
    return res
