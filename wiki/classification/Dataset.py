from sklearn.model_selection import train_test_split

from information_extraction.nlpUtils import nlpUtils
from db_data import WikiArtistDAO as art_DAO, WikiCategoryDAO as cat_DAO
from db_data import GraphDAO as graph_DAO
import csv
import pandas as pd
from sklearn.utils import shuffle

# favorite, inspired, influenced, listen

def bufferize_articles():
    buffer = list()
    for artist in art_DAO.find_all():
        buffer.append(artist)
    return buffer


def select_section(corpus, selectors, inverse_selection):
    selected_sections = list()
    sections = corpus.split("\n\n")
    for section in sections:
        for sentence in section.split("\n"):
            if sentence != "" and sentence[-1] not in [".",":"] and len(sentence) < 40 and  "legacy" not in sentence:
                if inverse_selection is False and any(x in sentence for x in selectors):
                    selected_sections.append(section)
                    break
                elif inverse_selection is True and all(x not in sentence for x in selectors):
                    selected_sections.append(section)
                    break
    return selected_sections


#5803
def positives_1():
    nlp_utils = nlpUtils()
    positives  = list()
    for artist in bufferize_articles():
        style_sections =  select_section(artist["text"], ["influenc"], False)

        if style_sections.__len__() > 0:
            #print(artist["_id"])
            connections = list()
            for el in graph_DAO.linked_to(artist["_id"], "KNOWS", False):
                connections.append(el[1])
            #print(connections)
            for section in style_sections:
                positives.extend(nlp_utils.sentences_with_connections(section, connections, None))
    print(positives.__len__())
    return positives


def negatives_1():
    nlp_utils = nlpUtils()
    negatives  = list()
    for artist in bufferize_articles():
        if len(select_section(artist["text"], ["influenc"], False)) > 0:
            not_style_sections =  select_section(artist["text"], ["influenc"], True)
            if not_style_sections.__len__() > 0:
                connections = list()
                for el in graph_DAO.linked_to(artist["_id"], "KNOWS", False):
                    connections.append(el[1])
                for section in not_style_sections:
                    for sentence in nlp_utils.sentences_with_connections(section, connections, None):
                        if len(sentence)>70:
                            negatives.append(sentence)
                            print(" #  " +sentence)
    print(negatives.__len__())
    return negatives


def positives_2():
    nlp_utils = nlpUtils()
    positives = list()
    for artist in bufferize_articles():
        inflooenzers = list()
        for el in graph_DAO.linked_to(artist["_id"], "inflooenz_by", False):
            inflooenzers.append(el[1])
        print(inflooenzers)
        if len(inflooenzers) > 0:
            positives.extend(nlp_utils.sentences_with_connections(artist["text"], inflooenzers, None))
    print(positives.__len__())
    return positives


def negatives_2():
    nlp_utils = nlpUtils()
    negatives = list()
    for artist in bufferize_articles():
        connections = set()
        inflooenzers = set()
        for el in graph_DAO.linked_to(artist["_id"], "KNOWS", False):
            connections.add(el[1])
        for el in graph_DAO.linked_to(artist["_id"], "inflooenz_by", False):
            inflooenzers.add(el[1])
        not_inflooenzers = connections - inflooenzers

        if len(inflooenzers) > 0:
            negatives.extend(nlp_utils.sentences_with_connections(artist["text"], not_inflooenzers, None))
    print(negatives.__len__())
    return negatives



#462
def positives_3():
    nlp_utils = nlpUtils()
    positives = list()
    for artist in bufferize_articles():
        style_sections = select_section(artist["text"], ["influenc"], False)

        if style_sections.__len__() > 0:
            print(artist["_id"])
            connections = list()
            for el in graph_DAO.linked_to(artist["_id"], "inflooenz_by", False):
                connections.append(el[1])
            for section in style_sections:
                positives.extend(nlp_utils.sentences_with_connections(section, connections, None))

    print(positives.__len__())
    return positives


# 26746
def negatives_3():
    nlp_utils = nlpUtils()
    negatives = list()
    for artist in bufferize_articles():
        if len(select_section(artist["text"], ["influenc"], False)) > 0:
            not_style_sections = select_section(artist["text"], ["influenc"], True)
            if not_style_sections.__len__() > 0:
                connections = set()
                inflooenzers = set()
                for el in graph_DAO.linked_to(artist["_id"], "KNOWS", False):
                    connections.add(el[1])
                for el in graph_DAO.linked_to(artist["_id"], "inflooenz_by", False):
                    inflooenzers.add(el[1])
                not_inflooenzers = connections - inflooenzers

                for section in not_style_sections:
                    for sentence in nlp_utils.sentences_with_connections(section, not_inflooenzers, None):
                        if len(sentence)>70:
                            negatives.append(sentence)
                           # print(" #  " +sentence)

    print(negatives.__len__())
    return negatives


def writer():
    with open('/home/renzo/pos2.csv', mode= 'w') as file:
        for el in positives_2():
            writer = csv.writer(file)
            writer.writerow([el.replace("\"", "").replace("\n"," "), 1])




def create_training_test():
    pos= pd.read_csv('../data/pos3.csv', header=None)
    n_rows = pos.shape[0]
    print(n_rows)
    neg = pd.read_csv('../data/neg3.csv', header=None)
    neg = shuffle(neg)
    neg_undersampled = neg.sample(n=n_rows)

    dataset = shuffle(pd.concat([pos, neg_undersampled]))
    dataset.columns = ["text", "label"]

    training, test = train_test_split(dataset, test_size=0.15)

    for i in range(len(training)):
        training.iloc[i, 0] =  training.iloc[i, 0].replace("\n", " ")
    training.to_csv("../data/training_3.csv", sep=',', header=False, index=False)

    for i in range(len(test)):
        test.iloc[i, 0] =  test.iloc[i, 0].replace("\n", " ")
    test.to_csv("../data/test_3.csv", sep=',', header=False, index=False)

create_training_test()
