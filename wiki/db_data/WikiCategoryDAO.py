from db_data import DB as db


categories = db.get_mongo().categories_musical_groups

def insert(category):
   if not exists(category._id):
       categories.insert_one(category.__dict__)

def replace(category):
    categories.replace_one({'_id': category._id}, category.__dict__, upsert=True)

# returns a dict
def find(id):
    return categories.find_one({'_id': id})

def exists(id):
    return not categories.find({'_id': id}).count() == 0
