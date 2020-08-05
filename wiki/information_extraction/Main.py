from information_extraction.Relation_Extractor import Relation_Extractor
from db_data import WikiArtistDAO as art_DAO
from db_data import GraphDAO as graph_DAO
from information_extraction.nlpUtils import nlpUtils

relex = Relation_Extractor()
nlp_utils = nlpUtils()


for artist in art_DAO.find_by_linked(True):
    print("----------------------------------------")
    print(artist["_id"])
    first_sentence = nlp_utils.first_sentence(artist["text"])
    relex.extract_naitionalityAndType(first_sentence)

    res = graph_DAO.connections_from(artist["_id"], "KNOWS")
    connections = list()
    for record in res:
        connections.append(record["b"]["label"])

    if artist["label"] in connections:
        connections.remove(artist["label"])

    sent_list = nlp_utils.sentences_with_connections(artist["text"], connections, ['inspire', 'influenc'])
    for sent in sent_list:
        relex.extract_influencers(sent, connections)

    input("type something")

'''
frasi = list()
frasi.append("The band states that their main influences are Black Sabbath, Mercyful Fate, Forbidden and Iron Maiden.")
for frase in frasi:
    nlp_utils.analyze(frase)

'''