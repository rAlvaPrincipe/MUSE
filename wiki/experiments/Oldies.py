'''
def get_members2_v2(members, level, max_level):
    print("dentro+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    exclude_pages = ['Template:', "List of "]
    exclude_cats = ['boxes']
    pages = set()
    cats = set()
    for c in members.values():
        print(c.title)
        if c.ns == wikipediaapi.Namespace.CATEGORY and not any(x in c.title for x in exclude_cats):
            cats.add(c.title)
            if level < max_level:
                more_p, more_c = get_members2_v2(c.categorymembers, level=level + 1, max_level=max_level)
                pages.update(more_p)
                cats.update(more_c)
        elif c.ns == wikipediaapi.Namespace.MAIN and not any(x in c.title for x in exclude_pages):
            artist = WikiArtist(c)
            pages.add(artist)
    return pages, cats;
'''

'''
def get_members(members, level, max_level):
    exclude_pages = ['Template:', "List of "]
    exclude_cats = ['boxes']
    pages = set()
    for c in members.values():
        if c.ns == wikipediaapi.Namespace.CATEGORY and not any(x in c.title for x in exclude_cats):
            if level < max_level and c.title not in cats_done:
                cats_done.add(c.title)
                print("visiting: %s" % (c.fullurl))
                more_p = get_members(c.categorymembers, level=level + 1, max_level=max_level)
                pages.update(more_p)
        elif c.ns == wikipediaapi.Namespace.MAIN and not any(x in c.title for x in exclude_pages):
            pages.add(WikiArtist(c))
    return pages;
'''

'''
df_p = pd.DataFrame(pages.items(), columns=['page', 'count'])
df_c = pd.DataFrame(cats.items(), columns=['category', 'count'])
df = pd.read_csv("/home/renzo/dataframe_musicalgroups_6.csv",header=0)
df_p.to_csv('/home/renzo/pages_musicalGroups_10.csv', index=False)
df2 = df[(df['page'].str.contains("\(|\)")) & ( df['page'].str.contains("\(band\)|song\)|album\)|musician\)|band\)|EP\)|singer\)|group\)")==False)]
print(tabulate(df2, headers='keys', tablefmt='psql'))
'''

#json_object = json.dumps([ob.__dict__ for ob in list(pages)], indent=2)
#open("/home/renzo/Artists-data/groups-musicians-singers_level5.json", "a").write(json_object)


driver =  db.get_neo4j()
'''
user_input = ""
while user_input != "quit":
    user_input = input("\n\nDi chi vuoi sapere?: \n")
    page = wikipedia.page(title=user_input, auto_suggest=False)

    for link in page.links:
        if link in artists:
            print(link)
'''






'''
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "summaries+uni"))


def add_friend(tx, name, friend_name):
    tx.run("MERGE (a:Person {name: $name}) "
           "MERGE (b:Person {name: $friend_name}) "
           "MERGE (a)-[:KNOWS]->(b)",
           name=name, friend_name=friend_name)


def print_friends(tx, name):
    for record in tx.run("MATCH (a:Person)-[:KNOWS]->(friend) WHERE a.name = $name "
                         "RETURN friend.name ORDER BY friend.name", name=name):
        print(record["friend.name"])


with driver.session() as session:
    session.write_transaction(add_friend, "Arthur", "Guinevere")
    session.write_transaction(add_friend, "Arthur", "Lancelot")
    session.write_transaction(add_friend, "Arthur", "Merlin")
    session.write_transaction(add_friend, "Suca", "Guinevere")
    session.write_transaction(add_friend, "Suca", "Lancelot")
    session.write_transaction(add_friend, "Suca", "Merlin")
'''


''' ORIGNAL
def func():
    artists = set()
    for el in art_DAO.find_all():
        artists.add(el["label_ext"])

    with driver.session() as session:
        for el in art_DAO.find_all():
            print(el["label_ext"])
            page = wikipedia.page(title=el["label_ext"], auto_suggest=False)
            for link in page.links:
                if link in artists:
                    session.write_transaction(add_relation, el["label_ext"], link)



def add_relation(tx, name, friend_name):
    tx.run("MERGE (a:Person {name: $name}) "
           "MERGE (b:Person {name: $friend_name}) "
           "MERGE (a)-[:KNOWS]->(b)",
           name=name, friend_name=friend_name)
'''

'''
def create_graph():
    artists = set()
    for el in art_DAO.find_all():
        artists.add(el["label_ext"])

    buffer = list()
    buffer_dim = 1000
    for el in art_DAO.find_all():
        page = wikipedia.page(title=el["label_ext"], auto_suggest=False)
        effective_links = 0
        for link in page.links:
            if link in artists:
                effective_links += 1
                buffer.append((el["label_ext"], link))
        print("%s --> %d" % (el["_id"], effective_links))
        if effective_links == 0:
            buffer.append((el["label_ext"], None))
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" + page.title)

        if buffer.__len__() > buffer_dim:
            print("------------------- loading %d relations on neo4j" % (buffer_dim))
            art_DAO.insert(buffer)
            buffer.clear()
    print("--------------------- loading last relations on neo4j")
    art_DAO.executor(buffer)
'''


'''
#define the pattern
pattern = [{'DEP':'amod', 'OP':"?"}, # adjectival modifier
           {'POS':'NOUN'},
           {'LOWER': 'such'},
           {'LOWER': 'as'},
           {'POS': 'PROPN'}] #proper noun

# Matcher class object
matcher = Matcher(nlp.vocab)
matcher.add("matching_1", None, pattern)

matches = matcher(doc)
span = doc[matches[0][1]:matches[0][2]]

print(span.text)
'''


'''
    def analyze(self, sentence):
        df = pd.DataFrame(columns=("token", "POS", "dependency"))
        for tok in sentence:
            df = df.append({"token": tok.text, "POS": tok.pos_, "dependency" : tok.dep_}, ignore_index=True)
        print(tabulate(df, headers='keys', tablefmt='psql',showindex=False))

        df_ents = pd.DataFrame(columns=("token", "NER"))
        for ent in sentence.ents:
            df_ents  = df_ents.append({"token": ent.text, "NER": ent.label_}, ignore_index=True)
        print(tabulate(df_ents, headers='keys', tablefmt='psql',showindex=False))


    def match(self, pattern_name, patterns, doc):
        lista = list()
        matcher = Matcher(self.nlp.vocab)
        matcher.add(pattern_name, patterns)
        matches = matcher(doc)

        for start, end in matches:
            span = doc[start:end]  # The matched span
            lista.append(span.text)
        self.print_matches(doc.text, lista)
        return lista

'''

'''
nat_pattern = list()
#nationality.append([{'LEMMA': 'be'}, {'POS': 'DET'}, {'ENT_TYPE':{"IN":["GPE", "NORP", "LANGUAGE"]},'OP':"*"}, {"DEP":{"IN":["punct", "compound", "amod", "nmod"]}, "OP": "*"}, {'DEP': 'attr'}])
nat_pattern.append([{'LEMMA': 'be'}, {'POS': 'DET'}, {'ENT_TYPE':{"IN":["GPE", "NORP", "LANGUAGE"]},'OP':"*"},
                    {'POS':{"IN":["NOUN", "PROPN", "PUNCT","ADJ","SYM"]}, "OP":"*"}, {'POS':{"IN":["NOUN", "PROPN","ADJ"]}, "OP":"+"}])

#nationality.append([{'LEMMA': 'be'}, {'POS': 'DET'}, {'ENT_TYPE':{"IN":["GPE", "NORP", "LANGUAGE"]},'OP':"*"}, {"DEP":{"IN":["punct", "compound", "amod", "nmod"]}, "OP": "*"}, {'POS': 'NOUN'}, {"POS":{"IN":["PUNCT", "NOUN", "ADJ", "PROPN"]}, "OP": "*"}, {'ORTH': 'and'},  {'POS': 'ADJ', "OP":"*"}, {'POS':{"IN":["NOUN", "PROPN"]}, "OP":"*"}, {'DEP': 'conj', "OP":"+"}])
nat_pattern.append([{'LEMMA': 'be'}, {'POS': 'DET'}, {'ENT_TYPE':{"IN":["GPE", "NORP", "LANGUAGE"]},'OP':"*"},
                    {"DEP":{"IN":["punct", "compound", "amod", "nmod"]}, "OP": "*"}, {'POS': 'NOUN'}, {"POS":{"IN":["PUNCT", "NOUN", "ADJ", "PROPN"]}, "OP": "*"}, {'ORTH': 'and'},
                    {'POS':{"IN":["NOUN", "PROPN", "PUNCT","ADJ"]}, "OP":"*"}, {'POS':{"IN":["NOUN", "PROPN","ADJ"]}, "OP":"+"}])




#  match("birthplace", [{'ENT_TYPE': 'GPE'}], nlp(sentence.text))

'''