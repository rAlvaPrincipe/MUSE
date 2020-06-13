from information_extraction.Relation_Extractor import Relation_Extractor
from DB import WikiArtistDAO as art_DAO

relex = Relation_Extractor()
'''
for artist in art_DAO.find_all(None):
    #input("\npress anyhting")
    print("-----------------------------------------------------------------------------------------------------------------------")
    first_sentence = relex.first_sentence(artist["text"])
    relex.extract_naitionalityAndType(first_sentence)

'''

for artist in art_DAO.find_all(True):
    print("----------------------------------------")
    print(artist["_id"])
    res = art_DAO.connections_from(artist["_id"])
    connections = list()
    for record in res:
        connections.append(record["b"]["label"])

    if artist["label"] in connections:
        connections.remove(artist["label"])

    print(connections)
    relex.sentences_with_connections(artist["text"], connections)
    input("type something")
