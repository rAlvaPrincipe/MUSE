import DB as db

artists = db.get_mongo().musicians

def find_all():
    return artists.find({})


def find_by_label_ext(label_ext):
    return artists.find_one({'label_ext': label_ext})

def replace(artist):
    if type(artist) is dict:
        artists.replace_one({'_id': artist["_id"]}, artist, upsert=True)
    else:
        artists.replace_one({'_id': artist._id}, artist.__dict__, upsert=True)

