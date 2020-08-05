from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
import pickle
from information_extraction.nlpUtils import nlpUtils


def preprocessing(df, featurize):
    nlp_utils = nlpUtils()
    if(featurize):
        for i in range(len(df)):
            df.iloc[i, 0] = nlp_utils.featurize(df.iloc[i, 0])

    return df["text"].tolist(), df["label"].tolist()


def training_test(dataset):
    training, test = train_test_split(dataset, test_size=0.3)
    # print(tabulate(training, headers='keys', tablefmt='psql', showindex=False))
    # print(tabulate(test, headers='keys', tablefmt='psql', showindex=False))
    training_X = training["text"].tolist()
    training_Y = training["label"].tolist()
    test_X = test["text"].tolist()
    test_Y = test["label"].tolist()
    return training_X, training_Y, test_X, test_Y


# --------------------------------------------------------------------------------------------

def gs_nb(training_X, training_Y):
    nb_clf = Pipeline([('vect', CountVectorizer()),
                         ('tfidf', TfidfTransformer()),
                         ('clf', MultinomialNB())])

    parameters = {'vect__ngram_range': [(1, 1), (1, 2), (1, 3), (1, 4)],
                  'tfidf__use_idf': (True, False),
                  'clf__alpha': (1, 1e-1, 1e-2, 1e-3),
                  'clf__fit_prior': (True, False)
                  }

    gs_clf = GridSearchCV(nb_clf, parameters, n_jobs=-1)
    gs_clf = gs_clf.fit(training_X, training_Y)
    print(gs_clf.best_params_)
    print(gs_clf.best_score_)
    return gs_clf.best_estimator_


def gs_svm(training_X, training_Y):
    svm_clf = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', SGDClassifier(tol=None))])

    parameters = {'vect__ngram_range': [(1, 1), (1, 2), (1, 3), (1, 4)],
                  'tfidf__use_idf': (True, False),
                  'clf__max_iter': (5, 10, 50, 100),
                  'clf__penalty': ('l2', 'elasticnet'),
                  'clf__alpha': (1e-2, 1e-3, 1e-4, 1e-5)
                  }

    gs_clf = GridSearchCV(svm_clf, parameters, n_jobs=-1)
    gs_clf = gs_clf.fit(training_X, training_Y)
    print(gs_clf.best_params_)
    print(gs_clf.best_score_)
    return gs_clf.best_estimator_


def compare_models(best_nb, best_svm, training_X, training_Y):
    accuray_nb = cross_val_score(best_nb, training_X, training_Y, cv=6)
    accuracy_svm = cross_val_score(best_svm, training_X, training_Y, cv=6)
    print("Accuracy--------------------------------")
    print("nb: ", accuray_nb.mean())
    print("svm: ", accuracy_svm.mean())

    precision_nb = cross_val_score(best_nb, training_X, training_Y, cv=6, scoring='precision')
    precision_svm = cross_val_score(best_svm, training_X, training_Y, cv=6, scoring='precision')
    print("Precision--------------------------------")
    print("nb: ", precision_nb.mean())
    print("svm: ",precision_svm.mean())

    recall_nb = cross_val_score(best_nb, training_X, training_Y, cv=6, scoring='recall')
    recall_svm = cross_val_score(best_svm, training_X, training_Y, cv=6, scoring='recall')
    print("Recall--------------------------------")
    print("nb: ", recall_nb.mean())
    print("svm: ", recall_svm.mean())

    if precision_nb.mean() > precision_svm.mean():
        return best_nb
    else:
        return best_svm



def training():
    training = pd.read_csv('../data/training_3_corretto.csv', header=None)
    training.columns = ["text", "label"]

    print("preprocessing training dataset ----------------")
    training_X, training_Y = preprocessing(training, True)

    print("Grid Search Naive Bayes ----------------")
    best_nb = gs_nb(training_X, training_Y)
    print("Grid Search SVM ----------------")
    best_svm = gs_svm(training_X, training_Y)
    print("Comparing models ----------------")
    best_model = compare_models(best_nb, best_svm, training_X, training_Y)

    #pickle.dump(best_model, open("../data/pickle_handmade_training.model", 'wb'))



#training()