import pandas as pd
import spacy
from tabulate import tabulate
from colorama import Fore, Style

class nlpUtils:

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")


    def doc_from_text(self, text):
        return self.nlp(text)


    # takes corpus(string) and return the first sentence(string)
    def first_sentence(self, corpus):
        corpus.translate(str.maketrans({"\n": " ", "\t": " ", "\r": " "})).replace("  ", " ")
        with self.nlp.disable_pipes("ner", "tagger"):
            doc = self.nlp(corpus)
            for sent in doc.sents:
                sent_text = sent.text
                if '.' not in sent_text[-3:]:
                    for el in list(doc.sents)[1:]:
                        sent_text += " " + el.text
                        if '.' in el.text[-2:]:
                            break
                return sent_text


    # take string and print analysis
    def analyze(self, sentence):
        df = pd.DataFrame(columns=("token", "POS", "dependency"))
        doc = self.nlp(sentence)
        for tok in doc:
            df = df.append({"token": tok.text, "POS": tok.pos_, "dependency" : tok.dep_}, ignore_index=True)
        print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))

     #   df_ents = pd.DataFrame(columns=("token", "NER"))
     #   for ent in doc.ents:
     #       df_ents  = df_ents.append({"token": ent.text, "NER": ent.label_}, ignore_index=True)
     #   print(tabulate(df_ents, headers='keys', tablefmt='psql', showindex=False))


    # take a list of tuples (spans, id) and return clean lists (spans and text)
    def clean(self, matches):
        tuple_list = list()
        text_list = list()
        for tuple_i in matches:
            span_i = tuple_i[0]
            keep = True
            for tuple_j in matches:
                span_j = tuple_j[0]
                if span_i.text != span_j.text:
                    if span_i.text in span_j.text:
                        keep = False
                        break;
            if keep:
                tuple_list.append(tuple_i)
                text_list.append(span_i.text)

        return text_list, tuple_list


    # takes string and a not empty list of matches. Colors the matches. Support one match at time
    def print_matches(self, sentence, matches_list):
        if matches_list.__len__() > 0:
            biggest_match = max(matches_list, key=len)
            start = sentence.index(biggest_match)
            print(sentence[:start], end="")
            print(Fore.RED + biggest_match, end="")
            print(Style.RESET_ALL, end="")
            print(sentence[start + len(biggest_match):])

            #  for match in matches_list:
            #     print(Fore.BLUE, match)
            print(Style.RESET_ALL, end="")
        else:
            print(sentence)


    def print_matches_multiple(self, sent, matches_list):
        first = ""
        indx_first = 0
        while indx_first != 10000:
            indx_first = 10000
            for el in matches_list:
                if el in sent:
                    if sent.index(el) < indx_first:
                        first = el
                        indx_first = sent.index(el)

            if indx_first != 10000:
                start = sent.index(first)
                print(sent[:start], end="")
                print(Fore.RED + first, end="")
                print(Style.RESET_ALL, end="")
                sent = sent[start + len(first):]

            else:
                print(sent)


    def sentences_with_connections(self, corpus, connections, selectors_list):
        sent_list = list()
        corpus.translate(str.maketrans({"\n": " ", "\t": " ", "\r": " "})).replace("  ", " ")
        with self.nlp.disable_pipes("ner", "tagger"):
            doc = self.nlp(corpus)
            for sent in doc.sents:
                citations = list()
                for connection in connections:
                    if connection in sent.text:
                        citations.append(connection)

                if len(citations) > 0:
                    if selectors_list is not None:
                        for el in selectors_list:
                            if el in sent.text:
                                sent_list.append(sent.text)
                              #  self.print_matches_multiple(sent.text, citations)
                                #self.analyze(sent.text)
                                break
                    else:
                        sent_list.append(sent.text)
                     #   self.print_matches_multiple(sent.text, citations)
        return sent_list


    def featurize(self, sentence):
        #print(sentence)
        doc = self.nlp(sentence)
        sentence_featurized = ""
        for tok in doc:
            sentence_featurized +=  tok.text + " " + tok.lemma_ + " "
       # print(sentence_featurized)
        return sentence_featurized



    def remove_strings(self, sentence, to_remove, replacement):
        output = sentence
        print(output)
        for el in to_remove:
            if el in output:
                output = output.replace(el, replacement)
        print(output)
        return output



