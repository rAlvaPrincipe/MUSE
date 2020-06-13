import spacy
from spacy.matcher.matcher import Matcher
import pandas as pd
from tabulate import tabulate
from colorama import Fore, Style

class Relation_Extractor:

    def __init__(self):
        self.df = pd.read_csv("../data/countries.csv")
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



    # We assume that types are commma separated. Nationality can be declared immediatly before types or in the form "from <Country>"
    def extract_naitionalityAndType(self, sentence):
        #x, matches = self.match("nationality_type", sentence) # la funzione deve andare bene per tutti i tipi di match!
        match = self.match(sentence)   # looking for string that matches both nationality and types in an adjacent way or just types
        if match is not None:
            self.print_matches(sentence, [match.text])
            countries = self.get_countries_from_match(match)  #this kind of information is always in one single span
            types = self.get_types_from_match(match)
            print(countries)
            print(types)
        else:
            print(sentence)
            print("NO MATCHES")
       # if nationalities is empty:
        #    nationality_matches = match("nationality2", sentence)
        # nationalities = extract a list of nationalities from  nationalities_matches
        #return nationalities, types


# -------------------------------------------- MATCHING  -------------------------------------------------------------------------

    def get_countries_from_match(self, match):
        nationalities = list()
        for ent in match.ents:
            if ent.label_ in ["NORP", "GPE", "LANGUAGE"]:
                country = self.nationality_to_country(ent.text)
                if country is not None:
                    nationalities.append(country)
        return nationalities


    def get_types_from_match(self, match):
        types = list()
        type = ""
        prev_tok = ""
        for tok in match:
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


    # take string and returns the first significative match
    def match(self, sentence):
        doc = self.nlp(sentence)
        matches = self.nationality_matcher(doc)
        lista_spans = list()
        for id, start, end in matches:
            span = doc[start:end]  # The matched span
            lista_spans.append(span)

        # clean matches and extract the first match since is often the significative one
        text_list, span_list = self.clean(lista_spans)
        indx = 1000
        span_out = None
        for span in span_list:
            if span[0].i < indx:
                indx = span[0].i
                span_out = span

        return span_out


    # take string and print analysis
    def analyze(self, sentence):
        df = pd.DataFrame(columns=("token", "POS", "dependency"))
        doc = self.nlp(sentence)
        for tok in doc:
            df = df.append({"token": tok.text, "POS": tok.pos_, "dependency" : tok.dep_}, ignore_index=True)
        print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))

        df_ents = pd.DataFrame(columns=("token", "NER"))
        for ent in doc.ents:
            df_ents  = df_ents.append({"token": ent.text, "NER": ent.label_}, ignore_index=True)
        print(tabulate(df_ents, headers='keys', tablefmt='psql', showindex=False))


    #takes string and return string
    def nationality_to_country(self, nationality):
        res = self.df[self.df['nationality'].str.lower() == nationality.lower()].reset_index()
        if res.shape[0] > 0:
            return res.get_value(0, 'en_short_name')
        return None
    #Dovremmoe farlo con un dictionary. Scandiamo il csv/json riga/document  alla volta, processiamo e creiamo un key value da mettere nel dict


#-------------------------------------------- UTILS -------------------------------------------------------------------------

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


    def sentences_with_connections(self, corpus, connections):
        corpus.translate(str.maketrans({"\n": " ", "\t": " ", "\r": " "})).replace("  ", " ")
        with self.nlp.disable_pipes("ner", "tagger"):
            doc = self.nlp(corpus)
            for sent in doc.sents:
                citations = list()
                for connection in connections:
                    if connection in sent.text:
                        citations.append(connection)
                        #self.print_matches(sent.text, [connection] )
                        #for tok in sent:
                        #    if tok.dep_ == "ROOT":
                        #        print(tok.lemma_)
                        #break
                if len(citations) > 0:
                    self.print_matches_multiple(sent.text, citations)


    # take a list of matches (spans) and return clean lists (spans and text)
    def clean(self, matches):
        span_list = list()
        text_list = list()
        for span_i in matches:
            keep = True
            for span_j in matches:
                if span_i.text != span_j.text:
                    if span_i.text in span_j.text:
                        keep = False
                        break;
            if keep:
                span_list.append(span_i)
                text_list.append(span_i.text)

        return text_list, span_list


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

