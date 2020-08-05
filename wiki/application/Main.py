import pymongo
import requests
import wikipediaapi
import wikipedia
from  builtins import any

from classification.Predictor import Predictor
from db_data.WikiArtist import WikiArtist
from db_data import WikiArtistDAO as art_DAO, WikiCategoryDAO as cat_DAO
from db_data import GraphDAO as graph_DAO
from db_data.WikiCategory import WikiCategory
from information_extraction.Relation_Extractor import Relation_Extractor
from information_extraction.nlpUtils import nlpUtils

wiki = wikipediaapi.Wikipedia('en', extract_format=wikipediaapi.ExtractFormat.WIKI)
exclude_pages = ["Template:", "List of ", "album)", "EP)", "song)", "film)", "comedian)", "video)", "videography", "discography", "filmography", "(disambiguation)" ]
exclude_cats = ['boxes', 'albums', 'films', 'songs','Albums', 'Films', 'Songs', 'templates', 'tours', 'album covers', "band)", "duo)", "trio)"]

# given a set of categories/pages and a max depth visit this func save text and metadata about wiki pages
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


def process_buffer(buffer, waiting4linking, relation):
    if relation == "inflooenz_by":
        graph_DAO.influenced_by(buffer, "inflooenz_by")
        for el in waiting4linking:
            el['linked_inflooenz'] = True
            art_DAO.replace(el)
    elif relation == "inf_ML_by":
        graph_DAO.influenced_by(buffer, "inf_ML_by")
        for el in waiting4linking:
            el['linked_ML'] = True
            art_DAO.replace(el)
    elif relation == "inf_patterns_by":
        graph_DAO.influenced_by(buffer, "inf_patterns_by")
        for el in waiting4linking:
            el['linked_patterns'] = True
            art_DAO.replace(el)
    elif relation == "related_to":
        graph_DAO.insert_node2(buffer)
        for el in waiting4linking:
            el['linked'] = True
            art_DAO.replace(el)
    buffer.clear()
    waiting4linking.clear()


def get_URI_disambiguated(el, connections, duplicates):
    find = False
    el_URI = None
    for related_artist in connections:
        if related_artist[1] == el:
            el_URI = related_artist[0]
            find = True
            break
    if not find and el not in duplicates:
        el_dic = art_DAO.find_by_label(el)
        if el_dic is not None:
            el_URI = el_dic["_id"]
    return el_URI


# avoid tables in wiki articles
def create_graph_no_tables():
    artists = set()
    for el in art_DAO.find_all():
        artists.add(el["label_ext"])

    buffer = list()
    waiting4linking = list()
    buffer_dim = 10
    try:
        for el in art_DAO.find_by_linked(False):
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
                    process_buffer(buffer, waiting4linking, "related_to")
            except (ConnectionError, KeyError, wikipedia.exceptions.DisambiguationError, wikipedia.exceptions.PageError) as e:
                print('----------- connection ERROR or Page ERROR ' +  el['_id'])

        print("--------------------- loading last relations on neo4j")
        process_buffer(buffer, waiting4linking, "related_to")
    except (pymongo.errors.CursorNotFound, requests.exceptions.ConnectionError) :
        print('------------------- CursorNotFound Error: ' + el['_id'])
        create_graph_no_tables()


def link_artist_infloeenz():
    duplicates = art_DAO.duplicate_labels()
    buffer = list()
    waiting4linking = list()
    buffer_dim = 100
    try:
        for artist in art_DAO.find_by_linked_inflooenz(False):
            print(artist["_id"])
            influencers = artist["inflooenz_influences"]
            followers = artist["inflooenz_followers"]
            if type(influencers) is list:
                if len(influencers) > 0 or len(followers) > 0: # to avoid connections finding when not necessary
                    connections = graph_DAO.related_to(artist["_id"], True)
                    for el in influencers:
                        influencer_URI = get_URI_disambiguated(el, connections, duplicates)
                        if influencer_URI is not None:
                            buffer.append((artist["_id"], influencer_URI))
                    if type(followers) is list:
                        for el in followers:
                            follower_URI = get_URI_disambiguated(el, connections, duplicates)
                            if follower_URI is not None:
                                buffer.append((follower_URI, artist["_id"]))
                waiting4linking.append(artist) # only artist with 0 or more influences are checked. Uncertain artist are not considered
            if waiting4linking.__len__() > buffer_dim:
                print("------------------- loading relations about %d artists on neo4j" % (buffer_dim))
                process_buffer(buffer, waiting4linking, "inflooenz_by")
        print("--------------------- loading last relations on neo4j")
        process_buffer(buffer, waiting4linking, "inflooenz_by")
    except (pymongo.errors.CursorNotFound):
        print('------------------- CursorNotFound Error: ' + artist['_id'])
        link_artist_infloeenz()


def link_artists_patterns():
    relex = Relation_Extractor()
    nlp_utils = nlpUtils()
    duplicates = art_DAO.duplicate_labels()
    buffer = list()
    waiting4linking = list()
    buffer_dim = 100
    try:
        for artist in art_DAO.find_by_linked_patterns(False):
            print("----_" + artist["label_ext"])
            connections = graph_DAO.related_to(artist["_id"], False)
            connections_only_label = list()
            for el in connections:
                 connections_only_label.append(el[1])

            influencers = set()
            sent_list = nlp_utils.sentences_with_connections(artist["text"], connections_only_label, ['inspire', 'influenc'])
            for sent in sent_list:
                sent_influencers = relex.extract_influencers(sent, connections_only_label)
                if sent_influencers is not None:
                    influencers.update(sent_influencers)

            for influencer in influencers:
                influencer_URI = get_URI_disambiguated(influencer, connections, duplicates)
                print(influencer_URI)
                buffer.append((artist["_id"], influencer_URI))

            waiting4linking.append(artist)
            if waiting4linking.__len__() > buffer_dim:
                print("------------------- loading relations about %d artists on neo4j" % (buffer_dim))
                process_buffer(buffer, waiting4linking, "inf_patterns_by")
        print("--------------------- loading last relations on neo4j")
        process_buffer(buffer, waiting4linking, "inf_patterns_by")
    except (pymongo.errors.CursorNotFound):
        print('------------------- CursorNotFound Error: ' + artist['_id'])
        link_artists_patterns()


def link_artists_distant_supervision():
    nlp_utils = nlpUtils()
    relex = Relation_Extractor()
    predictor = Predictor()
    duplicates = art_DAO.duplicate_labels()
    buffer = list()
    waiting4linking = list()
    buffer_dim = 100
    try:
        for artist in art_DAO.find_by_linked_ML(False):
            print("----_" + artist["label_ext"])
            connections = graph_DAO.related_to(artist["_id"], False)
            connections_only_label = list()
            for el in connections:
                connections_only_label.append(el[1])

            influencers = set()
            sent_list = nlp_utils.sentences_with_connections(artist["text"], connections_only_label, None)   # not limited to "inspired" and "influenced" ones because the ML model is supposed to works with every "influenced_by" representation
            for sent in sent_list:
                sent_featurized = nlp_utils.featurize(sent)
                prediction = predictor.predict_sentence(sent_featurized)[0]
                if prediction == 1:
                    sent_influencers = relex.get_artist_from_sentence(sent, connections_only_label)
                    if sent_influencers is not None:
                        influencers.update(sent_influencers)
            for influencer in influencers:
                influencer_URI = get_URI_disambiguated(influencer, connections, duplicates)
                print(influencer_URI)
                buffer.append((artist["_id"], influencer_URI))

            waiting4linking.append(artist)
            if waiting4linking.__len__() > buffer_dim:
                print("------------------- loading relations about %d artists on neo4j" % (buffer_dim))
                process_buffer(buffer, waiting4linking, "inf_ML_by")
        print("--------------------- loading last relations on neo4j")
        process_buffer(buffer, waiting4linking, "inf_ML_by")
    except (pymongo.errors.CursorNotFound):
        print('------------------- CursorNotFound Error: ' + artist['_id'])
        link_artists_distant_supervision()


def bufferize_articles():
    buffer = list()
    for artist in art_DAO.find_all():
        buffer.append(artist)
    return buffer

'''
members_seed = dict()
for cat in ["Category:Singers"]: #"Category:Musical groups", "Category:Musicians", "Category:Singers"
    members_seed.update(wiki.page(cat).categorymembers)

get_articles(members_seed, 0, 30)
print("done")
'''

#create_graph_no_tables()
#link_artist_infloeenz()
#link_artists_patterns()


'''
artist = art_DAO.find_by_label_ext(input())
result  = graph_DAO.connections_to(artist["_id"], "inflooenz_by")
for record  in result:
    print((record["b"]["URL"], record["b"]["label"]))
result  = graph_DAO.connections_to(artist["_id"], "INF_by")
for record  in result:
    print((record["b"]["URL"], record["b"]["label"]))

'''

link_artists_distant_supervision()