import pandas as pd
import pickle
from sklearn.metrics import recall_score, accuracy_score, precision_score, f1_score
from classification.Learning import preprocessing
from information_extraction.Relation_Extractor import Relation_Extractor
import os

class Predictor:

    def __init__(self):
        path = os.path.dirname(os.path.realpath(__file__))
        self.loaded_model = pickle.load(open(os.path.join(path, "../data/pickle_handmade_training.model"), 'rb'))
        self.test_set_file = os.path.join(path, "../data/test_3_corretto_v2.csv")


    def scores(self, y_true, y_predicted):
        print("accuracy: ", accuracy_score(y_true, y_predicted))
        print("precision: ", precision_score(y_true, y_predicted))
        print("recall: ", recall_score(y_true, y_predicted))
        print("f-measure: ", f1_score(y_true, y_predicted))


    def supervised_model_testing(self):
        print("Testing distant supervised model -------")
        test = pd.read_csv(self.test_set_file, header=None)
        test.columns = ["text", "label"]

        print("preprocessing test dataset ----------------")
        test_X, test_Y = preprocessing(test, True)
        predicted_Y = self.loaded_model.predict(test_X)
        self.scores(test_Y, predicted_Y)

        copy = pd.read_csv(self.test_set_file, header=None)
        copy.columns = ["text", "label"]
        for i in range(len(test_X)):
            print(test_Y[i], predicted_Y[i],  copy["text"][i])

        #for i in range(len(y_predicted)):
        #    print(y_predicted[i], test_Y[i])


    def pattern_based_testing(self):
        print("Testing pattern based model -------")
        relex = Relation_Extractor()
        test = pd.read_csv(self.test_set_file, header=None)
        test.columns = ["text", "label"]
        test_Y = test["label"].tolist()

        predicted_Y = list()
        for index, row in test.iterrows():
            match = relex.match(row['text'], "influencedBy")
            if match is None:
                predicted_Y.append(0)
            else:
                predicted_Y.append(1)
        self.scores(test_Y, predicted_Y)

        copy = pd.read_csv(self.test_set_file, header=None)
        copy.columns = ["text", "label"]
        for i in range(len(test)):
            print(test_Y[i], predicted_Y[i],  copy["text"][i])

    def predict_sentence(self, sentence):
        return self.loaded_model.predict([sentence])

predictor = Predictor()
#predictor.supervised_model_testing()
predictor.pattern_based_testing()