from db_data import DB as db

artists = db.get_mongo().all_artists


def find_all():
    return artists.find({})

def find_by_linked(linked):
    if linked:
        return artists.find({"linked": True})
    elif linked is False:
        return artists.find({"linked": False})

def find_by_linked_inflooenz(linked_inflooenz):
    if linked_inflooenz:
        return artists.find({"linked_inflooenz": True})
    elif linked_inflooenz is False:
        return artists.find({"linked_inflooenz": False})

def find_by_linked_patterns(linked_patterns):
    if linked_patterns:
        return artists.find({"linked_patterns": True})
    elif linked_patterns is False:
        return artists.find({"linked_patterns": False})

def find_by_linked_ML(linked_ML):
    if linked_ML:
        return artists.find({"linked_ML": True})
    elif linked_ML is False:
        return artists.find({"linked_ML": False})



# returns a dict
def find_by_id(id):
    return artists.find_one({'_id': id})

def find_by_label_ext(label_ext):
    return artists.find_one({'label_ext': label_ext})

def find_by_label(label):
    return artists.find_one({'label': label})

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


def duplicate_labels():
    labels = set()
    labels_duplicates = set()
    for artist in find_all():
        label = artist["label"]
        if label in labels:
            labels_duplicates.add(label)
        else:
            labels.add(label)
    return labels_duplicates


#for el in find_all():
#    el["linked_inflooenz"] = False
#    replace(el)


#for el in find_all():
#    el["linked_patterns"] = False
#    replace(el)

#for el in find_all():
#    el["linked_ML"] = False
#    replace(el)