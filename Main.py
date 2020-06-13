import pymongo
import requests
import wikipediaapi
import wikipedia
from  builtins import any
from DB.WikiArtist import WikiArtist
from DB import WikiArtistDAO as art_DAO, WikiCategoryDAO as cat_DAO
from DB.WikiCategory import WikiCategory

wiki = wikipediaapi.Wikipedia('en', extract_format=wikipediaapi.ExtractFormat.WIKI)
exclude_pages = ["Template:", "List of ", "album)", "EP)", "song)", "film)", "comedian)", "video)", "videography", "discography", "filmography", "(disambiguation)" ]
exclude_cats = ['boxes', 'albums', 'films', 'songs','Albums', 'Films', 'Songs', 'templates', 'tours', 'album covers', "band)", "duo)", "trio)"]
#driver = db.get_neo4j()

def get_articles(members, level, max_level):
    open("/home/renzo/Artists-data/levels_singers.txt", "a").write("  "+str(level)+"\n")
    for c in members.values():
        if c.ns == wikipediaapi.Namespace.CATEGORY and not any(x in c.title for x in exclude_cats):
            if level < max_level:
                if cat_DAO.exists(c.fullurl) is False or cat_DAO.find(c.fullurl)['status'] == 'visiting':
                    wiki_cat = WikiCategory(c, "visiting")
                    cat_DAO.insert(wiki_cat)
                    print("visiting: %s" % (c.fullurl))
                    open("/home/renzo/Artists-data/levels_singers.txt", "a").write(str(c.fullurl))
                    get_articles(c.categorymembers, level=level + 1, max_level=max_level)
                    wiki_cat.status = "visited"
                    cat_DAO.replace(wiki_cat)
        elif c.ns == wikipediaapi.Namespace.MAIN and not any(x in c.title for x in exclude_pages):
            art_DAO.insert(WikiArtist(c))



def process_buffer(buffer, waiting4linking):
    art_DAO.insert_node2(buffer)
    for el in waiting4linking:
        el['linked'] = True
        art_DAO.replace(el)
    buffer.clear()
    waiting4linking.clear()

# avoid tables in wiki articles
def create_graph_no_tables():
    artists = set()
    for el in art_DAO.find_all(None):
        artists.add(el["label_ext"])

    buffer = list()
    waiting4linking = list()
    buffer_dim = 10
    try:
        for el in art_DAO.find_all(False):
            try:
                page = wikipedia.page(title=el["label_ext"], auto_suggest=False)
                text = el['text']
                effective_links = 0
                for link in page.links:
                    if link in artists:
                        label = link
                        if label[-1] == ')':
                            label = label[:label.rfind(" (")]
                        if label in text:
                            effective_links += 1
                            buffer.append((el, art_DAO.find_by_label_ext(link)))

                print("%s --> %d" % (el["_id"], effective_links))
                if effective_links == 0:
                    buffer.append((el, None))

                waiting4linking.append(el)
                if waiting4linking.__len__() > buffer_dim:
                    print("------------------- loading relations about %d artists on neo4j" % (buffer_dim))
                    process_buffer(buffer, waiting4linking)
            except (ConnectionError, KeyError, wikipedia.exceptions.DisambiguationError, wikipedia.exceptions.PageError) as e:
                print('----------- connection ERROR or Page ERROR ' +  el['_id'])

        print("--------------------- loading last relations on neo4j")
        process_buffer(buffer, waiting4linking)
    except (pymongo.errors.CursorNotFound, requests.exceptions.ConnectionError) :
        print('------------------- CursorNotFound Error: ' + el['_id'])
        create_graph_no_tables()




'''
members_seed = dict()
for cat in ["Category:Singers"]: #"Category:Musical groups", "Category:Musicians", "Category:Singers"
    members_seed.update(wiki.page(cat).categorymembers)

get_articles(members_seed, 0, 30)
print("done")
'''

create_graph_no_tables()

'''
art_DAO.connections_from("Ramones")
print("--------------------------------")
art_DAO.connections_to("Ramones")
'''
