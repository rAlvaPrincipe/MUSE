import spacy
from spacy.matcher.matcher import Matcher
import pandas as pd
from information_extraction.nlpUtils import nlpUtils
import os

class Relation_Extractor:

    def __init__(self):
        path = os.path.dirname(os.path.realpath(__file__))
        self.df = pd.read_csv(os.path.join(path,"../data/countries.csv"))
        self.utils = nlpUtils()
        self.nlp = spacy.load("en_core_web_sm")
        self.nationality_matcher = Matcher(self.nlp.vocab)
        nat_pattern = list()
        nat_pattern.append(
            [{'LEMMA': 'be'}, {'POS': 'DET'}, {'ENT_TYPE': {"IN": ["GPE", "NORP", "LANGUAGE"]}, 'OP': "*"},
             {'POS': {"IN": ["NOUN", "PROPN", "PUNCT", "ADJ", "SYM"]}, "OP": "*"},
             {'POS': {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"}])
        nat_pattern.append(
            [{'LEMMA': 'be'}, {'POS': 'DET'}, {'ENT_TYPE': {"IN": ["GPE", "NORP", "LANGUAGE"]}, 'OP': "*"},
             {"DEP": {"IN": ["punct", "compound", "amod", "nmod"]}, "OP": "*"}, {'POS': 'NOUN'},
             {"POS": {"IN": ["PUNCT", "NOUN", "ADJ", "PROPN"]}, "OP": "*"}, {'ORTH': 'and'},
             {'POS': {"IN": ["NOUN", "PROPN", "PUNCT", "ADJ"]}, "OP": "*"},
             {'POS': {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"}])

        self.nationality_matcher.add("nationality", nat_pattern)


        self.influence_matcher = Matcher(self.nlp.vocab)

        influence1 = list()
        influence1.append([{'LEMMA': {"IN": ["inspire", "influence"]}, "POS": 'VERB'}, {'ORTH': 'by'}, {"OP": "*"}])
        self.influence_matcher.add("influence1", influence1)

        influence2 = list()
        influence2.append([{'LEMMA': {"IN": ["cite", "refer", "list", "mention", "credit","claim"]}, "POS": 'VERB'}, {"OP": "*"}, {'LEMMA':{"IN": ["as", "among"]}}, {"OP": "*"},{'LEMMA': 'influence', "POS": 'NOUN'}, {"OP": "*"}])
        influence2.append([{'LEMMA': {"IN": ["cite", "refer", "list", "mention", "credit","claim"]}, "POS": 'VERB'}, {"OP": "*"}, {'LEMMA': 'be'}, {"OP": "*"},{'LEMMA': 'influence', "POS": 'NOUN'}])
        self.influence_matcher.add("influence2", influence2)

        influence3 = list()
        influence3.append([{'LEMMA': 'influence', "POS": 'NOUN'}, {'ORTH': 'include', "POS": 'VERB'}, {"OP": "*"}])
        self.influence_matcher.add("influence3", influence3)

        influence4 = list()
        influence4.append([{'ORTH': 'influences', "POS": 'NOUN'}, {'ORTH': 'cited'}, {'ORTH': 'by'}, {"OP": "*"}, {'ORTH': 'include', "POS": 'VERB'}, {"OP": "*"}])
        self.influence_matcher.add("influence4", influence4)

        influence5 = list()
        influence5.append([{'LEMMA': 'cite', "POS": 'VERB'}, {'ORTH': ','}, {"ORTH": "as"}, {"OP": "*"}, {'ORTH': 'influences', "POS": 'NOUN'},  {"OP": "*"}])
        self.influence_matcher.add("influence5", influence5)

        influence6 = list()
        influence6.append([{'LEMMA': 'state', "POS": 'VERB'}, {"OP": "*"}, {'LEMMA': 'influence', "POS": 'NOUN'}, {'LEMMA': 'be'}, {"OP": "*"}])
        self.influence_matcher.add("influence6", influence6)

        influence7 = list()
        influence7.append([{'ORTH': 'influences', "POS": 'NOUN'}, {"ORTH": "?"}, {"ORTH": "such"}, {"ORTH": "as"}, {"OP": "*"}])
        self.influence_matcher.add("influence7", influence7)

        influence8 = list()
        influence8.append([{'LEMMA': {"IN": ["cite", "name"]}, "POS": "VERB"}, {"OP": "*"}, {"ORTH": "as"}, {"ORTH": "one"}, {"ORTH": "of"},  {"OP": "*"},  {"ORTH": "'s"}, {'LEMMA': 'influence', "POS": 'NOUN'}])
        self.influence_matcher.add("influence8", influence8)

        influence9 = list()
        influence9.append([{'LEMMA': 'influence', "POS": 'NOUN'}, {"ORTH": "including"}, {"OP": "*"}])
        self.influence_matcher.add("influence9", influence9)

        influence10 = list()
        influence10.append([{'LEMMA': 'influence', "POS": 'NOUN'}, {"OP": "*"}, {"ORTH": "from"}, {"OP": "*"}])
        self.influence_matcher.add("influence10", influence10)

        influence11 = list()
        influence11.append([{'ORTH': 'citing', "POS": 'VERB'}, {"ORTH": "as"}, {'LEMMA': 'influence', "POS": 'NOUN'}, {"OP": "*"}])
        self.influence_matcher.add("influence11", influence11)

        influence12 = list()
        influence12.append([{'LEMMA': 'influence', "POS": 'NOUN'}, {'LEMMA': 'be'}, {"OP": "*"}])
        self.influence_matcher.add("influence12", influence12)

        influence13 = list()
        influence13.append([{'LEMMA': 'influence', "POS": 'NOUN'}, {'ORTH': 'of'}, {"OP": "*"}])
        self.influence_matcher.add("influence13", influence13)

        influence14 = list()
        influence14.append([{'LEMMA': 'inspiration', "POS": 'NOUN'}, {'ORTH': {"IN": ["from", "include"]}}, {"OP": "*"}])
        influence14.append([{'LEMMA': 'cite', "POS": 'VERB'}, {"OP": "*"}, {"ORTH": "as"}, {'LEMMA': 'inspiration', "POS": 'NOUN'}])
        self.influence_matcher.add("influence14", influence14)

        self.mappa = dict()
        self.mappa[self.nlp.vocab.strings["influence1"]] = "influence1"
        self.mappa[self.nlp.vocab.strings["influence2"]] = "influence2"
        self.mappa[self.nlp.vocab.strings["influence3"]] = "influence3"
        self.mappa[self.nlp.vocab.strings["influence4"]] = "influence4"
        self.mappa[self.nlp.vocab.strings["influence5"]] = "influence5"
        self.mappa[self.nlp.vocab.strings["influence6"]] = "influence6"
        self.mappa[self.nlp.vocab.strings["influence7"]] = "influence7"
        self.mappa[self.nlp.vocab.strings["influence8"]] = "influence8"
        self.mappa[self.nlp.vocab.strings["influence9"]] = "influence9"
        self.mappa[self.nlp.vocab.strings["influence10"]] = "influence10"
        self.mappa[self.nlp.vocab.strings["influence11"]] = "influence11"
        self.mappa[self.nlp.vocab.strings["influence12"]] = "influence12"
        self.mappa[self.nlp.vocab.strings["influence13"]] = "influence13"
        self.mappa[self.nlp.vocab.strings["influence14"]] = "influence14"


    # takes a tuple (match, id)
    def get_countries_from_match(self, match):
        nationalities = list()
        for ent in match[0].ents:
            if ent.label_ in ["NORP", "GPE", "LANGUAGE"]:
                country = self.nationality_to_country(ent.text)
                if country is not None:
                    nationalities.append(country)
        return nationalities


    # takes a tuple (match, id)
    def get_types_from_match(self, match):
        types = list()
        type = ""
        prev_tok = ""
        for tok in match[0]:
            if (tok.orth_ == "and" or tok.orth_ == ",") and type != "":
                types.append(type)
                type = ""
            if tok.ent_type_ not in ["NORP", "GPE", "LANGUAGE"] and tok.lemma_ != "be" and tok.pos_ != "DET" and tok.orth_ != "and" and tok.orth_ != ",":
                if type == "" or tok.text in ["-","/"] or prev_tok.text in["-","/"]:
                    type += tok.text
                else:
                    type += " " + tok.text
            prev_tok = tok
        if type != "":
            types.append(type)

        return types


    # takes a tuple (match, id)
    def get_influencers_from_match(self, match, connections):
        return self.get_artist_from_sentence(match[0].text, connections)


    def get_artist_from_sentence(selfself, sentence, connections):
        influencers = list()
        for connection in connections:
            if connection in sentence:
                influencers.append(connection)
        return influencers


    # take sentence (String) and relation try the match and return a coupe (span, id) where id is the pattern id which matches
    def match(self, sentence, relation):
        doc = self.utils.doc_from_text(sentence)
        if relation == "nationality":
            matches = self.nationality_matcher(doc)
        else:
            matches = self.influence_matcher(doc)

        lista_spans = list()
        for id, start, end in matches:
            span = doc[start:end]  # The matched span
            lista_spans.append((span, id))

        # clean matches and extract the first match since is often the significative one  for nationality
        # for influence relation 1 match is enaugh
        text_list, span_list = self.utils.clean(lista_spans)
        indx = 1000
        span_out = None
        for couple in span_list:
            span = couple[0]
            if span[0].i < indx:
                indx = span[0].i
                span_out = (span, couple[1])
        return span_out



    #takes string and return string
    def nationality_to_country(self, nationality):
        res = self.df[self.df['nationality'].str.lower() == nationality.lower()].reset_index()
        if res.shape[0] > 0:
            return res.get_value(0, 'en_short_name')
        return None
    #Dovremmoe farlo con un dictionary. Scandiamo il csv/json riga/document  alla volta, processiamo e creiamo un key value da mettere nel dict



    # We assume that types are commma separated. Nationality can be declared immediatly before types or in the form "from <Country>"
    def extract_naitionalityAndType(self, sentence):
        # x, matches = self.match("nationality_type", sentence) # la funzione deve andare bene per tutti i tipi di match!
        match = self.match(sentence, "nationality")  # looking for string that matches both nationality and types in an adjacent way or just types
        if match is not None:
            self.utils.print_matches(sentence, [match[0].text])
            countries = self.get_countries_from_match(match)  # this kind of information is always in one single span
            types = self.get_types_from_match(match)
            print(countries)
            print(types)
        else:
            print(sentence)
            print("NO MATCHES")
    # if nationalities is empty:
    #    nationality_matches = match("nationality2", sentence)
    # nationalities = extract a list of nationalities from  nationalities_matches
    # return nationalities, types


    def extract_influencers(self, sentence, connections):
        match = self.match(sentence, "influencedBy")
        influencers = None
        if match is not None:
           # self.utils.print_matches(sentence, [match[0].text])
            influencers = self.get_influencers_from_match(match, connections)
           # print(influencers)
        return influencers


