from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from tabulate import tabulate
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

# https://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html

categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']
twenty_train = fetch_20newsgroups(subset="train", categories=categories, shuffle=True, random_state=42)

# ------------------------------------ Training a model -------------------------------------------------------
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(twenty_train.data)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

#print(X_train_tfidf)
#print(type(X_train_tfidf))
#clf = MultinomialNB().fit(X_train_tfidf, twenty_train.target)

'''
# ------------------------------------ Training a model using a pipeline ---------------------------------------
test_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', MultinomialNB())])

test_clf.fit(twenty_train.data, twenty_train.target)

# ------------------------------------ predicting on 2 sentences -----------------------------------------------
docs_new = ['God is love.', "OpenGL on the GPU is fast"]
X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)
for doc, category in zip(docs_new, predicted):
    print('%r => %s' % (doc, twenty_train.target_names[category]))

# --------------------------------------predicting on test set--------------------------------------------
twenty_test = fetch_20newsgroups(subset="test", categories=categories, shuffle=True, random_state=42)
docs_test = twenty_test.data
predicted = test_clf.predict(docs_test)
for doc, category in zip(docs_test, predicted):
    print('%r \n %s' % (doc, twenty_test.target_names[category]))

print(np.mean(predicted == twenty_test.target))

# ------------------------------------ SVM prediction ---------------------------------------------------

svm_clf = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, random_state=42, max_iter=5, tol=None))
])

svm_clf.fit(twenty_train.data, twenty_train.target)
predicted = svm_clf.predict(docs_test)
print(np.mean(predicted == twenty_test.target))
'''
#-----------------------------------------------------------------------------------------------
'''
docs_train = ["ciao bello", "ciao zio", "ciao scemo", "bella ciao", "ciao babbo", "ciao pirla", "addio tizio", "addio mami", "suca cane", "che ne so", "addio gatto"]
docs_label = [1,1,1,1,1,1,0,0,0,0,0]
docs_test = ["ciao nonno", "hey amico ciao", "addio cojone", "boh, suca", "cioè ciao ti spacco la faccia", "ciao mami", "addio bellissimo"]
count_vect = CountVectorizer()
tfidf_transformer = TfidfTransformer()
test_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', MultinomialNB())])
test_clf.fit(docs_train, docs_label)

#X_new_counts = count_vect.transform(docs_test)
#X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = test_clf.predict(docs_test)
for doc, category in zip(docs_test, predicted):
    print('%r => %s' % (doc, category))
'''


tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words='english')
features = tfidf.fit_transform(twenty_train.data).toarray()
print(features.shape)
print(type(features))
print(features)